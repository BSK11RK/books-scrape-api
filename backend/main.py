# 認証API
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
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

# ログ初期化
logger = setup_logging()

app = FastAPI(title="JWT Auto Scraper Portfolio")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.on_event("startup")
def startup_event():
    logger.info("アプリ起動")
    start()

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
        logger.warning("ログイン失敗")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": form_data.username})
    logger.info(f"ログイン成功: {form_data.username}")
    return {"access_token": token, "token_type": "bearer"}

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        logger.error("トークン検証失敗")
        raise HTTPException(status_code=401)

@app.get("/books")
def get_books(current_user: str = Depends(get_current_user)):
    logger.info(f"/books 実行 by {current_user}")
    
    books = scrape_books()
    save_all_formats(books)
    generate_graph(books)
    
    return {"user": current_user, "count": len(books)}

@app.get("/")
def root():
    return {"message": "JWT Scraper Running"}