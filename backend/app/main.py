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


# API 起動時に DB テーブルを用意するアプリ全体の入口処理
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


# FastAPI の入力検証エラーを共通エラー形式に変換する
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


# DB 層の例外を API 共通レスポンスの 500 エラーに変換する
@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_response(
            "DATABASE_ERROR",
            "データベース処理中にエラーが発生しました。",
        ),
    )


# 稼働確認用の軽量なヘルスチェックエンドポイント
@app.get("/health")
def health() -> dict:
    return success_response({"status": "ok"})
