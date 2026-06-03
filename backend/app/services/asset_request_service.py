from datetime import UTC, datetime

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


class ActiveAssetRequestNotFoundError(AssetRequestError):
    code = "ACTIVE_REQUEST_NOT_FOUND"
    status_code = 404


class AssetRequestReturnError(AssetRequestError):
    code = "ASSET_REQUEST_NOT_RETURNABLE"
    status_code = 409


class AssetRequestCancelError(AssetRequestError):
    code = "ASSET_REQUEST_NOT_CANCELABLE"
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

        consuming_quantity = db.scalar(
            select(func.coalesce(func.sum(AssetRequest.quantity), 0)).where(
                AssetRequest.asset_id == payload.asset_id,
                AssetRequest.status.in_(
                    [
                        AssetRequestStatus.pending,
                        AssetRequestStatus.loaned,
                    ]
                ),
            )
        )
        available_quantity = asset.total_stock - int(consuming_quantity or 0)

        if available_quantity < payload.quantity:
            raise InsufficientReservedStockError("現在、他の方が申請中または貸出中のため在庫が不足しています")

        asset_request = AssetRequest(
            asset_id=payload.asset_id,
            user_id=1,
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


def list_active_asset_requests(db: Session, user_id: int = 1) -> list[tuple[AssetRequest, Asset]]:
    return list(
        db.execute(
            select(AssetRequest, Asset)
            .join(Asset, Asset.id == AssetRequest.asset_id)
            .where(
                AssetRequest.user_id == user_id,
                AssetRequest.status.in_(
                    [
                        AssetRequestStatus.loaned,
                        AssetRequestStatus.pending,
                    ]
                ),
            )
            .order_by(AssetRequest.end_date.asc(), AssetRequest.id.asc())
        ).all()
    )


def return_asset_request(db: Session, request_id: int, user_id: int = 1) -> AssetRequest:
    with db.begin():
        asset_request = db.scalar(
            select(AssetRequest)
            .where(
                AssetRequest.id == request_id,
                AssetRequest.user_id == user_id,
            )
            .with_for_update()
        )

        if asset_request is None:
            raise ActiveAssetRequestNotFoundError("対象の貸出申請が見つかりません。")

        if asset_request.status != AssetRequestStatus.loaned:
            raise AssetRequestReturnError("貸出中の備品のみ返却できます。")

        asset_request.status = AssetRequestStatus.returned
        asset_request.returned_at = datetime.now(UTC)
        db.flush()
        db.refresh(asset_request)

        return asset_request


def cancel_asset_request(db: Session, request_id: int, user_id: int = 1) -> AssetRequest:
    with db.begin():
        asset_request = db.scalar(
            select(AssetRequest)
            .where(
                AssetRequest.id == request_id,
                AssetRequest.user_id == user_id,
            )
            .with_for_update()
        )

        if asset_request is None:
            raise ActiveAssetRequestNotFoundError("対象の貸出申請が見つかりません。")

        if asset_request.status != AssetRequestStatus.pending:
            raise AssetRequestCancelError("承認待ちの申請のみキャンセルできます。")

        asset_request.status = AssetRequestStatus.cancelled
        db.flush()
        db.refresh(asset_request)

        return asset_request
