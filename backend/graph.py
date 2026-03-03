import os, logging
import pandas as pd
import matplotlib.pyplot as plt
from backend.config import DATA_DIR

logger = logging.getLogger(__name__)

def generate_graph(books: list):

    if not books:
        logger.warning("グラフ生成スキップ（データなし）")
        return

    try:
        prices = [b["price"] for b in books]

        plt.figure(figsize=(10, 6))
        plt.hist(prices, bins=10)
        plt.title("Book Price Distribution", fontsize=16)
        plt.xlabel("Price", fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.grid(True, linestyle="--", alpha=0.5)

        png_path = os.path.join(DATA_DIR, "books.png")
        plt.savefig(png_path, dpi=300)
        plt.close()

        logger.info("グラフ生成完了")

    except Exception as e:
        logger.error(f"グラフ生成エラー: {e}")