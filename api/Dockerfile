# ローカル開発環境用ステージ
FROM python:3.10-slim as local

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV ENVIRONMENT=local \
  PYTHONPATH=/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# 本番環境（AWS Lambda）用ステージ
FROM public.ecr.aws/lambda/python:3.10 as production

# 依存関係のインストール
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# アプリケーションコードのコピー
COPY app ${LAMBDA_TASK_ROOT}/app
COPY app/main.py ${LAMBDA_TASK_ROOT}/

# 環境変数の設定
ENV ENVIRONMENT=production \
  AWS_LAMBDA_FUNCTION_NAME=sample-api

CMD ["app.main.handler"]

# デフォルトは本番環境用のステージを使用
FROM production
