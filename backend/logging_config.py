# logging設定ファイル作成
import os, logging
from logging.handlers import RotatingFileHandler
from backend.config import LOG_DIR

LOG_FILE = os.path.join(LOG_DIR, "app.log")

def setup_logging():
    logger =logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # フォーマット
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    
    # ファイル出力
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)
    
    # コンソール出力
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger