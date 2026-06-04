from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.asset_request import AssetRequestStatus


class AssetRequestCreate(BaseModel):
    asset_id: int = Field(ge=1)
    requester_name: str = Field(min_length=1, max_length=120)
    start_date: date
    end_date: date
    reason: str = Field(min_length=1)
    quantity: int = Field(ge=1)

    @model_validator(mode="after")
    def validate_date_range(self) -> "AssetRequestCreate":
        if self.end_date < self.start_date:
            raise ValueError("終了日は開始日以降の日付を指定してください。")
        return self


class AssetRequestRead(BaseModel):
    id: int
    asset_id: int
    user_id: int
    requester_name: str
    start_date: date
    end_date: date
    reason: str
    quantity: int
    status: AssetRequestStatus
    returned_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActiveAssetRequestRead(AssetRequestRead):
    asset_name: str
    asset_category: str
