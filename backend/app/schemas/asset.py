from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AssetBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    status: str = Field(default="available", min_length=1, max_length=40)


class AssetCreate(AssetBase):
    current_stock: int = Field(ge=1)


class AssetRead(AssetBase):
    id: int
    current_stock: int = Field(ge=0)
    pending_quantity: int = Field(ge=0)
    effective_stock: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AssetPage(BaseModel):
    items: list[AssetRead]
    total: int = Field(ge=0)
    total_count: int = Field(ge=0)
    total_stock: int = Field(ge=0)
    low_stock_count: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_pages: int = Field(ge=1)
