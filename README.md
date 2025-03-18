# FastAPI Lambda サンプルプロジェクト

このプロジェクトは、FastAPI アプリケーションをローカル環境（Docker Compose）と AWS Lambda 環境の両方で同一コードベースとして運用するためのサンプルです。

## 機能

- ヘルスチェックエンドポイント (`/health`)
- サンプルデータ処理エンドポイント (`/process`)
- 環境に応じた動的 CORS 設定
- マルチステージ Docker ビルド対応

## 必要要件

- Python 3.10 以上
- Docker
- Docker Compose v2
- AWS CLI（本番環境デプロイ時）

## ディレクトリ構造

```
fastapi-lambda-sample/
├── README.md
├── api/
│   ├── Dockerfile
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── models.py
│   └── requirements.txt
└── compose.yaml
```

## セットアップ方法

### ローカル環境

1. プロジェクトディレクトリに移動：

```bash
cd fastapi-lambda-sample
```

2. Docker Compose で環境を起動：

```bash
docker compose up
```

3. API の動作確認：

```bash
# ヘルスチェック
curl http://localhost:8000/health

# サンプルデータ処理
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"data": "test"}'
```

### AWS Lambda 環境へのデプロイ

1. 本番用 Docker イメージをビルド：

```bash
docker build -t sample-api:production ./api
```

2. AWS ECR にプッシュ：

```bash
aws ecr get-login-password --region ap-northeast-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com
docker tag sample-api:production $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/sample-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.ap-northeast-1.amazonaws.com/sample-api:latest
```

3. AWS Lambda の環境変数を設定：

- `ENVIRONMENT`: `production`
- `API_KEY`: 任意のセキュアな値
- `DEBUG`: `False`
- `LOG_LEVEL`: `INFO`

## 開発方法

1. ローカル環境の起動：

```bash
docker compose up
```

2. コードの変更を行う（ホットリロードが有効）

3. テストの実行：

```bash
docker compose exec api pytest
```

## 環境変数

| 変数名      | 説明                            | デフォルト値 | 必須 |
| ----------- | ------------------------------- | ------------ | ---- |
| ENVIRONMENT | 実行環境 (`local`/`production`) | `local`      | ○    |
| API_KEY     | API キー                        | -            | ○    |
| DEBUG       | デバッグモード                  | `False`      | ×    |
| LOG_LEVEL   | ログレベル                      | `INFO`       | ×    |

## ライセンス

MIT

## 作者

example
