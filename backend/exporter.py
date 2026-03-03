import os, logging
import pandas as pd
from backend.database import SessionLocal
from backend.models import Book
from backend.config import DATA_DIR

logger = logging.getLogger(__name__)

def save_all_formats(books: list):

    if not books:
        logger.warning("保存対象データがありません")
        return

    df = pd.DataFrame(books)

    # パス定義
    csv_path = os.path.join(DATA_DIR, "books.csv")
    json_path = os.path.join(DATA_DIR, "books.json")
    excel_path = os.path.join(DATA_DIR, "books.xlsx")

    try:
        # CSV
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        # JSON
        df.to_json(json_path, orient="records", force_ascii=False, indent=2)

        # Excel
        df.to_excel(excel_path, index=False)

        logger.info("CSV / JSON / Excel 保存完了")

    except Exception as e:
        logger.error(f"ファイル保存エラー: {e}")
        return

    # DB保存
    db = SessionLocal()

    try:
        # 既存データ削除
        db.query(Book).delete()

        # 新規追加
        for book in books:
            db.add(Book(**book))

        db.commit()
        logger.info("DB保存完了")

    except Exception as e:
        db.rollback()
        logger.error(f"DB保存エラー: {e}")

    finally:
        db.close()