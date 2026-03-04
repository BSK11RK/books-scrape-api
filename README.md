# 📚 JWT Async Scraper API

FastAPI + PostgreSQL + Dockerで構築した非同期スクレイピング対応の認証付きREST APIです。

実務を想定し、認証・権限制御・非同期処理・テスト・ログ設計まで実装しています。

---

# 🚀 主な機能

- JWT認証（ログイン / 登録）
- 管理者専用スクレイピング実行API
- 非同期スクレイピング（httpx + asyncio）
- PostgreSQL永続化
- 重複防止（Upsert処理）
- ページネーション
- 価格フィルタ
- ソート機能
- BackgroundTasksによる非同期実行
- pytest + fixtureによる高度テスト
- ログ出力（運用想定）

---

# 🏗 システム構成

```
Client
   ↓
FastAPI (JWT認証)
   ↓
PostgreSQL
   ↑
Background Task
   ↓
Async Scraper (httpx + asyncio)
```

---

# 🛠 システム構成

- FastAPI
- PostgreSQL
- SQLAlchemy
- Docker / Docker Compose
- httpx (async)
- BeautifulSoup
- python-jose (JWT)
- pytest

---

# 📦 環境構築手順

## 1. Clone

```bash
git clone <your-repository-url>
cd <project-folder>
```

## 2. .env 作成

```env
ENV=development

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=books_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

DATABASE_URL=postgresql://postgres:postgres@db:5432/books_db

SECRET_KEY=supersecretkey_change_me
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

## 3. 起動

```bash
docker compose up --build
```

APIドキュメント:
```
http://localhost:8000/docs
```

---

# 🔐 Authentication

## ユーザー登録

```
POST /register
```

## ログイン

```
POST /login
```

返却される `access_token` を使用:

```
Authorization: Bearer <token>
```

---

# 📚 API一覧

## 管理者専用スクレイピング

```
POST /scrape
```

- 管理者のみ実行可能
- BackgroundTasksで非同期実行
- DBにUpsert保存

---

## 書籍一覧取得

```
GET /books
```

### Query Parameters

| Parameter   | Description |
|-------------|-------------|
| limit       | 取得件数（最大100） |
| offset      | 開始位置 |
| min_price   | 最小価格フィルタ |
| max_price   | 最大価格フィルタ |
| sort        | price_asc / price_desc |

---

# 🧪 テスト

pytestで実装しました。

実行方法:

```bash
docker compose exec app pytest
```

### テスト内容

- JWT認証テスト
- 管理者権限チェック
- ページネーション検証
- フィルタ検証
- fixtureによるDB分離テスト

---

# 📊 データ永続化

- PostgreSQLで永続化
- 重複タイトルは更新（Upsert）
- Dockerコンテナ間接続

---

# 📈 ログ機能

- スクレイピング開始/終了ログ
- ページ取得ログ
- エラーハンドリングログ
- DB保存ログ

運用を想定したログ設計です。

---

# 🔄 ログ機能

- httpx.AsyncClient使用
- asyncio.gatherで並列取得
- 50ページ同時取得
- 高速化対応

---

# 🔒 セキュリティ

- JWT認証
- 管理者専用エンドポイント
- 環境変数による機密管理
- .envは.gitignore管理

---

# 📂 プロジェクト構成

```
backend/
 ├── main.py
 ├── database.py
 ├── models.py
 ├── auth.py
 ├── scraper.py
 ├── exporter.py
 ├── scheduler.py
 ├── logging_config.py
 └── config.py

tests/
 ├── conftest.py
 ├── test_main.py
 └── test_advanced.py
```

---

# 🌱 今後の改善点

- CI/CD (GitHub Actions)
- Redis + Celeryによる本格ジョブキュー化
- フロントエンド追加
- 本番環境デプロイ（Render / Railway）
- API rate limit
- OpenAPI仕様書整備

---

# 🎯 今後の改善点

実務を想定したバックエンドAPI設計のポートフォリオです。

- 認証
- DB設計
- 非同期処理
- テスト
- Docker運用

を一貫して実装しました。

---

# 👤 Author

Your Name

---

# 🏁 まとめ

FastAPIを用いた実践的なバックエンドAPI構築例です。

認証・非同期処理・DB永続化・テストまで一通り実装し、実務レベルの構成を目指しました。