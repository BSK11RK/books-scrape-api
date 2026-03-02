import os
import pandas as pd
from backend.database import SessionLocal, Book
from backend.config import DATA_DIR

def save_all_formats(books: list):

    if not books:
        print("No books to save.")
        return

    df = pd.DataFrame(books)

    # パス定義
    csv_path = os.path.join(DATA_DIR, "books.csv")
    json_path = os.path.join(DATA_DIR, "books.json")
    excel_path = os.path.join(DATA_DIR, "books.xlsx")

    # CSV保存
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")

    # JSON保存
    df.to_json(json_path, orient="records", force_ascii=False, indent=2)

    # Excel保存
    df.to_excel(excel_path, index=False)

    # DB保存
    db = SessionLocal()

    try:
        # 既存データ削除
        db.query(Book).delete()

        # 新規追加
        for book in books:
            db.add(Book(**book))

        db.commit()

    except Exception as e:
        db.rollback()
        print("DB Error:", e)

    finally:
        db.close()

    print("All formats saved successfully.")