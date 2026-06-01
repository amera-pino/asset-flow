from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.asset_request import AssetRequestCreate, AssetRequestRead
from app.schemas.response import ApiResponse, error_response, success_response
from app.services.asset_request_service import AssetRequestError, create_asset_request

router = APIRouter(prefix="/requests", tags=["requests"])


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
