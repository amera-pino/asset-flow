from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.asset_request import ActiveAssetRequestRead, AssetRequestCreate, AssetRequestRead
from app.schemas.response import ApiResponse, error_response, success_response
from app.services.asset_request_service import (
    AssetRequestError,
    cancel_asset_request,
    create_asset_request,
    list_active_asset_requests,
    return_asset_request,
)

router = APIRouter(prefix="/requests", tags=["requests"])
CURRENT_USER_ID = 1


@router.post("", response_model=ApiResponse[AssetRequestRead], status_code=201)
def create_request(
    payload: AssetRequestCreate,
    db: Annotated[Session, Depends(get_db)],
) -> dict | JSONResponse:
    try:
        asset_request = create_asset_request(db, payload)
    except AssetRequestError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.code, exc.message),
        )

    return success_response(AssetRequestRead.model_validate(asset_request))


@router.get("/me/active", response_model=ApiResponse[list[ActiveAssetRequestRead]])
def list_my_active_requests(db: Annotated[Session, Depends(get_db)]) -> dict:
    active_requests = [
        ActiveAssetRequestRead(
            **AssetRequestRead.model_validate(asset_request).model_dump(),
            asset_name=asset.name,
            asset_category=asset.category,
        )
        for asset_request, asset in list_active_asset_requests(db, CURRENT_USER_ID)
    ]

    return success_response(active_requests)


@router.post("/{request_id}/return", response_model=ApiResponse[AssetRequestRead])
def return_request(
    request_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> dict | JSONResponse:
    try:
        asset_request = return_asset_request(db, request_id, CURRENT_USER_ID)
    except AssetRequestError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.code, exc.message),
        )

    return success_response(AssetRequestRead.model_validate(asset_request))


@router.post("/{request_id}/cancel", response_model=ApiResponse[AssetRequestRead])
def cancel_request(
    request_id: int,
    db: Annotated[Session, Depends(get_db)],
) -> dict | JSONResponse:
    try:
        asset_request = cancel_asset_request(db, request_id, CURRENT_USER_ID)
    except AssetRequestError as exc:
        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(exc.code, exc.message),
        )

    return success_response(AssetRequestRead.model_validate(asset_request))
