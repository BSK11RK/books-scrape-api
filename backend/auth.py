# JWT認証・パスワードハッシュ
import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# 仮ユーザDB
fake_users_db = {
    "admin": {
        "username": "admin",
        "password": pwd_context.hash("admin123"),
        "role": "admin"
    }
}

# パスワードハッシュ化
def hash_password(password: str):
    return pwd_context.hash(password[:72])

# パスワード検証
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password[:72], hashed_password)

# JWT作成
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    return fake_users_db.get(username)

def add_user(username: str, password: str, role="user"):
    fake_users_db[username] = {
        "username": username,
        "password": password,
        "role": role
    }