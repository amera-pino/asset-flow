from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import get_settings


class Base(DeclarativeBase):
    pass


settings = get_settings()
engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables() -> None:
    import app.models  # noqa: F401

    Base.metadata.create_all(bind=engine)
    normalize_asset_request_status_column()


def normalize_asset_request_status_column() -> None:
    if engine.dialect.name != "postgresql":
        return

    statements = [
        "ALTER TABLE asset_requests ALTER COLUMN status DROP DEFAULT",
        "ALTER TABLE asset_requests ALTER COLUMN status TYPE VARCHAR(40) USING status::text",
        """
        UPDATE asset_requests
        SET status = CASE status
            WHEN '貸出中' THEN 'loaned'
            WHEN '返却済み' THEN 'returned'
            WHEN 'approved' THEN 'loaned'
            WHEN 'rejected' THEN 'cancelled'
            ELSE status
        END
        """,
        """
        UPDATE asset_requests
        SET status = 'cancelled'
        WHERE status NOT IN ('pending', 'loaned', 'returned', 'cancelled')
        """,
        "ALTER TABLE asset_requests DROP CONSTRAINT IF EXISTS ck_asset_requests_status_valid",
        """
        ALTER TABLE asset_requests
        ADD CONSTRAINT ck_asset_requests_status_valid
        CHECK (status IN ('pending', 'loaned', 'returned', 'cancelled'))
        """,
        "ALTER TABLE asset_requests ALTER COLUMN status SET DEFAULT 'pending'",
        "DROP TYPE IF EXISTS asset_request_status",
    ]

    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))
