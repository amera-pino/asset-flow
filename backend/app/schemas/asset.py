from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


# 備品 API の入出力で共通する名前・カテゴリ・状態の形
class AssetBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=80)
    status: str = Field(default="available", min_length=1, max_length=40)


# 備品登録 API 用の入力スキーマ
class AssetCreate(AssetBase):
    total_stock: int = Field(ge=1)


# 一覧・申請画面へ返す、在庫計算済みの備品レスポンス
class AssetRead(AssetBase):
    id: int
    total_stock: int = Field(ge=0)
    consuming_quantity: int = Field(ge=0)
    effective_stock: int = Field(ge=0)
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# 備品一覧画面のページング結果と集計値をまとめたレスポンス
class AssetPage(BaseModel):
    items: list[AssetRead]
    total: int = Field(ge=0)
    total_count: int = Field(ge=0)
    total_stock: int = Field(ge=0)
    low_stock_count: int = Field(ge=0)
    page: int = Field(ge=1)
    page_size: int = Field(ge=1)
    total_pages: int = Field(ge=1)
