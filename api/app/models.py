from pydantic import BaseModel, Field
from typing import Optional

class ProcessRequest(BaseModel):
    """データ処理リクエストモデル"""
    data: str = Field(..., description="処理対象のデータ")
    options: Optional[dict] = Field(default=None, description="処理オプション")

class ProcessResponse(BaseModel):
    """データ処理レスポンスモデル"""
    processed_data: str = Field(..., description="処理済みデータ")
    status: str = Field(..., description="処理ステータス")
    message: Optional[str] = Field(default=None, description="処理メッセージ")
