import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
from .models import ProcessRequest, ProcessResponse

# 環境変数の取得
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
API_KEY = os.getenv("API_KEY")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# FastAPIアプリケーションの初期化
app = FastAPI(
    title="Sample API",
    description="FastAPI Sample Application for Local and Lambda environments",
    version="1.0.0",
    debug=DEBUG
)

# CORS設定
ALLOWED_ORIGINS = (
    ["https://sample-app.example.com"] if ENVIRONMENT == "production"
    else ["http://localhost:3000"]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """ヘルスチェックエンドポイント"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT
    }

@app.post("/process", response_model=ProcessResponse)
async def process_data(request: ProcessRequest):
    """データ処理エンドポイント"""
    try:
        # サンプルの処理ロジック
        processed = request.data.upper()

        return ProcessResponse(
            processed_data=processed,
            status="success",
            message="データ処理が完了しました"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"データ処理中にエラーが発生しました: {str(e)}"
        )

# AWS Lambda環境の場合のみMangumハンドラーを作成
if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
    handler = Mangum(app, lifespan="off", api_gateway_base_path=None)
