from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.asset_request import AssetRequest, AssetRequestStatus
from app.schemas.asset_request import AssetRequestCreate


class AssetRequestError(Exception):
    code = "ASSET_REQUEST_ERROR"
    status_code = 400

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class AssetNotFoundError(AssetRequestError):
    code = "ASSET_NOT_FOUND"
    status_code = 404


class InsufficientReservedStockError(AssetRequestError):
    code = "INSUFFICIENT_STOCK"
    status_code = 409


def create_asset_request(db: Session, payload: AssetRequestCreate) -> AssetRequest:
    with db.begin():
        asset = db.scalar(
            select(Asset)
            .where(Asset.id == payload.asset_id)
            .with_for_update()
        )

        if asset is None:
            raise AssetNotFoundError("指定された備品が見つかりません。")

        pending_quantity = db.scalar(
            select(func.coalesce(func.sum(AssetRequest.quantity), 0)).where(
                AssetRequest.asset_id == payload.asset_id,
                AssetRequest.status == AssetRequestStatus.pending,
            )
        )
        available_quantity = asset.current_stock - int(pending_quantity or 0)

        if available_quantity < payload.quantity:
            raise InsufficientReservedStockError("現在、他の方が申請中のため在庫が不足しています")

        asset_request = AssetRequest(
            asset_id=payload.asset_id,
            requester_name=payload.requester_name,
            start_date=payload.start_date,
            end_date=payload.end_date,
            reason=payload.reason,
            quantity=payload.quantity,
            status=AssetRequestStatus.pending,
        )
        db.add(asset_request)
        db.flush()
        db.refresh(asset_request)

        return asset_request
