from fastapi import FastAPI, Depends, HTTPException, Query, BackgroundTasks
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import and_, asc, desc
from jose import jwt, JWTError

from backend.logging_config import setup_logging
import backend.config
from backend.auth import (
    hash_password,
    verify_password,
    create_access_token,
    SECRET_KEY,
    ALGORITHM,
    add_user,
    get_user
)
from backend.scraper import scrape_books
from backend.exporter import save_all_formats
from backend.graph import generate_graph
from backend.scheduler import start
from backend.database import SessionLocal, engine
from backend.models import Base, Book

# 初期設定
Base.metadata.create_all(bind=engine)

logger = setup_logging()

app = FastAPI(title="JWT Auto Scraper Portfolio")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB依存
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 起動時処理
@app.on_event("startup")
def startup_event():
    logger.info("アプリ起動")
    start()

# 認証
@app.post("/register")
def register(username: str, password: str):

    if get_user(username):
        logger.warning(f"既存ユーザー登録試行: {username}")
        raise HTTPException(status_code=400, detail="User exists")

    add_user(username, hash_password(password))
    logger.info(f"ユーザー登録成功: {username}")

    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = get_user(form_data.username)

    if not user or not verify_password(form_data.password, user["password"]):
        logger.warning(f"ログイン失敗: {form_data.username}")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})
    logger.info(f"ログイン成功: {form_data.username}")

    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        logger.error("JWT認証失敗")
        raise HTTPException(status_code=401)

# 重複防止（Upsert処理）
def save_books_to_db(db: Session):

    logger.info("スクレイピング開始")

    books = scrape_books()

    for b in books:
        existing = db.query(Book).filter(Book.title == b["title"]).first()

        if existing:
            existing.price = b["price"]
            existing.availability = b["availability"]
        else:
            new_book = Book(**b)
            db.add(new_book)

    db.commit()

    save_all_formats(books)
    generate_graph(books)

    logger.info(f"{len(books)}件のデータを保存完了")

# スクレイピング（管理者限定 + バックグラウンド）
@app.post("/scrape")
def run_scrape(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):

    # 簡易管理者チェック（adminのみ許可）
    if current_user != "admin":
        logger.warning(f"非管理者がscrape実行: {current_user}")
        raise HTTPException(status_code=403, detail="Admin only")

    background_tasks.add_task(save_books_to_db, db)

    logger.info(f"バックグラウンドでスクレイピング開始: {current_user}")

    return {"message": "Scraping started in background"}

# ページネーション + フィルタ + ソート
@app.get("/books")
def get_books(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),

    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),

    min_price: float | None = Query(None),
    max_price: float | None = Query(None),

    sort: str | None = Query(None),
):

    query = db.query(Book)

    # フィルタ
    conditions = []

    if min_price is not None:
        conditions.append(Book.price >= min_price)

    if max_price is not None:
        conditions.append(Book.price <= max_price)

    if conditions:
        query = query.filter(and_(*conditions))

    # ソート
    if sort == "price_asc":
        query = query.order_by(asc(Book.price))
    elif sort == "price_desc":
        query = query.order_by(desc(Book.price))

    total_count = query.count()

    books = query.offset(offset).limit(limit).all()

    logger.info(
        f"books取得: user={current_user}, total={total_count}, limit={limit}, offset={offset}"
    )

    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "count": len(books),
        "data": [
            {
                "id": b.id,
                "title": b.title,
                "price": b.price,
                "availability": b.availability,
            }
            for b in books
        ],
    }

@app.get("/")
def root():
    return {"message": "JWT Scraper Running"}