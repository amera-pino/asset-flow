from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.asset import Asset
from app.models.asset_request import AssetRequest, AssetRequestStatus
from app.schemas.asset import AssetPage, AssetRead
from app.schemas.response import ApiResponse, success_response

router = APIRouter(prefix="/assets", tags=["assets"])
ASSET_PAGE_SIZE = 20


@router.get("", response_model=ApiResponse[AssetPage])
def list_assets(
    db: Annotated[Session, Depends(get_db)],
    category: Annotated[str | None, Query(min_length=1, max_length=80)] = None,
    q: Annotated[str | None, Query(min_length=1, max_length=120)] = None,
    page: Annotated[int, Query(ge=1)] = 1,
    sort: Annotated[str | None, Query(pattern="^(name_asc|name_desc)$")] = None,
) -> dict:
    filters = []
    if category:
        filters.append(Asset.category == category)

    if q:
        filters.append(Asset.name.ilike(f"%{q}%"))

    pending_requests = (
        select(
            AssetRequest.asset_id,
            func.coalesce(func.sum(AssetRequest.quantity), 0).label("pending_quantity"),
        )
        .where(AssetRequest.status == AssetRequestStatus.pending)
        .group_by(AssetRequest.asset_id)
        .subquery()
    )
    pending_quantity = func.coalesce(pending_requests.c.pending_quantity, 0)

    total = db.scalar(select(func.count()).select_from(Asset).where(*filters)) or 0
    total_count = db.scalar(select(func.count()).select_from(Asset)) or 0
    total_stock = db.scalar(select(func.coalesce(func.sum(Asset.current_stock), 0))) or 0
    low_stock_count = (
        db.scalar(
            select(func.count())
            .select_from(Asset)
            .outerjoin(pending_requests, pending_requests.c.asset_id == Asset.id)
            .where((Asset.current_stock - pending_quantity) <= 5)
        )
        or 0
    )
    total_pages = max((total + ASSET_PAGE_SIZE - 1) // ASSET_PAGE_SIZE, 1)
    order_by_columns = (
        [Asset.name.asc(), Asset.id.asc()]
        if sort == "name_asc"
        else [Asset.name.desc(), Asset.id.desc()]
        if sort == "name_desc"
        else [Asset.created_at.desc(), Asset.id.desc()]
    )

    statement = (
        select(
            Asset,
            pending_quantity.label("pending_quantity"),
        )
        .outerjoin(pending_requests, pending_requests.c.asset_id == Asset.id)
        .where(*filters)
        .order_by(*order_by_columns)
        .limit(ASSET_PAGE_SIZE)
        .offset((page - 1) * ASSET_PAGE_SIZE)
    )

    assets = []
    for asset, pending_quantity in db.execute(statement).all():
        pending_quantity_value = int(pending_quantity or 0)
        assets.append(
            AssetRead(
                id=asset.id,
                name=asset.name,
                category=asset.category,
                status=asset.status,
                current_stock=asset.current_stock,
                pending_quantity=pending_quantity_value,
                effective_stock=max(asset.current_stock - pending_quantity_value, 0),
                created_at=asset.created_at,
                updated_at=asset.updated_at,
            )
        )

    return success_response(
        AssetPage(
            items=assets,
            total=total,
            total_count=total_count,
            total_stock=total_stock,
            low_stock_count=low_stock_count,
            page=page,
            page_size=ASSET_PAGE_SIZE,
            total_pages=total_pages,
        )
    )


@router.get("/categories", response_model=ApiResponse[list[str]])
def list_asset_categories(db: Annotated[Session, Depends(get_db)]) -> dict:
    categories = db.scalars(select(Asset.category).distinct().order_by(Asset.category.asc())).all()

    return success_response(list(categories))
