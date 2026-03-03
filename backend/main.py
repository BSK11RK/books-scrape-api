# 認証API
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import and_
from jose import jwt, JWTError
import logging

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

# テーブル作成
Base.metadata.create_all(bind=engine)

# ログ初期化
logger = setup_logging()

app = FastAPI(title="JWT Auto Scraper Portfolio")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# DB依存関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    logger.info("アプリ起動")
    start()

# 認証
@app.post("/register")
def register(username: str, password: str):
    if get_user(username):
        logger.warning("既存ユーザー登録試行")
        raise HTTPException(status_code=400, detail="User exists")
    
    add_user(username, hash_password(password))
    logger.info(f"ユーザー登録成功: {username}")
    return {"message": "User created"}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401)
    
# スクレイピング実行（重い処理）
@app.post("/scrape")
def run_scrape(current_user: str = Depends(get_current_user)):
    logging.info("スクレイピング手動実行")
    
    books = scrape_books()
    save_all_formats(books)
    generate_graph(books)
    
    return {"message": f"{len(books)}件取得しました"}

# ページネーション + フィルタ対応API
@app.get("/books")
def get_books(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
    
    # ページネーション
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    
    # フィルタ
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
):
    
    query = db.query(Book)
    
    # フィルタ条件追加 
    conditions = []
    
    if min_price is not None:
        conditions.append(Book.price >= min_price)
        
    if max_price is not None:
        conditions.append(Book.price <= max_price)
        
    if conditions:
        query = query.filter(and_(*conditions))
        
    # 総件数取得（フィルタ後）
    total_count = query.count()
    
    # ページネーション適用
    books = query.offset(offset).limit(limit).all()
    
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
                "availability": b.availability
            }
            for b in books
        ]
    }
        
@app.get("/")
def root():
    return {"message": "JWT Scraper Running"}