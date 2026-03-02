import os
import pandas as pd
import matplotlib.pyplot as plt
from backend.config import DATA_DIR

def generate_graph():

    df = pd.read_csv(os.path.join(DATA_DIR, "books.csv"))
    df["price"] = df["price"].str.replace("£", "").astype(float)
    
    plt.figure(figsize=(10, 6))
    plt.hist(df["price"], bins=10)
    plt.title("Book Price Distribution", fontsize=16)
    plt.xlabel("Price", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.grid(True, linestyle="--", alpha=0.5)
    
    plt.savefig(os.path.join(DATA_DIR, "books.png"), dpi=300)
    plt.close()