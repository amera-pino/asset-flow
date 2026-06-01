from typing import Any, Generic, TypeVar

from pydantic import BaseModel


DataT = TypeVar("DataT")


class ApiError(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ApiResponse(BaseModel, Generic[DataT]):
    success: bool
    data: DataT | None = None
    error: ApiError | None = None


def success_response(data: DataT) -> dict[str, Any]:
    return {"success": True, "data": data, "error": None}


def error_response(code: str, message: str, details: Any | None = None) -> dict[str, Any]:
    return {
        "success": False,
        "data": None,
        "error": {"code": code, "message": message, "details": details},
    }
