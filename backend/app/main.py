from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

from app.api.routes import assets, requests
from app.core.config import get_settings
from app.core.database import create_tables
from app.schemas.response import error_response, success_response


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield


settings = get_settings()

app = FastAPI(title="AssetFlow API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assets.router, prefix="/api")
app.include_router(requests.router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error_response(
            "VALIDATION_ERROR",
            "入力内容を確認してください。",
            exc.errors(),
        ),
    )


@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_response(
            "DATABASE_ERROR",
            "データベース処理中にエラーが発生しました。",
        ),
    )


@app.get("/health")
def health() -> dict:
    return success_response({"status": "ok"})
