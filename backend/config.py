# 共通パス管理
import os 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# dataフォルダを自動生成
os.makedirs(DATA_DIR, exist_ok=True)