# Dataset: https://www.kaggle.com/datasets/yousefsaeedian/financial-q-and-a-10k

# Output: data/processed/kaggle_clean.csv with columns context, ticker, year

import glob
import os
import re

import kagglehub
import pandas as pd

# downloads the datset and loads it 

path = kagglehub.dataset_download("yousefsaeedian/financial-q-and-a-10k")
csv_files = glob.glob(os.path.join(path, "**", "*.csv"), recursive=True)
print("CSV files found:", csv_files)

raw = pd.read_csv(csv_files[0])
print("Raw shape:", raw.shape)
print(raw.columns.tolist())

#cleaning the dataset
def clean_text(s: str) -> str:
    """Collapse whitespace/newlines and trim."""
    return re.sub(r"\s+", " ", str(s)).strip()


df = raw.copy()
df.columns = [c.strip().lower() for c in df.columns]

#Questions and answers are dropped on purpose so that chatbot not look at the answers to get bias results

df = df[["context", "ticker", "filing"]]

before = len(df)
df = df.dropna(subset=["context", "ticker"])
print(f"Dropped {before - len(df)} rows with missing context/ticker")

df["context"] = df["context"].map(clean_text)
df["ticker"] = df["ticker"].astype(str).str.strip().str.upper()

# Fiscal year from the filing column ("2023_10K" -> 2023)
df["year"] = df["filing"].astype(str).str.extract(r"(\d{4})")[0].astype("Int64")
df = df.drop(columns=["filing"])

before = len(df)
df = df[df["context"].str.len() >= 30]
print(f"Dropped {before - len(df)} very short contexts")

# Removes duplicate passages 
before = len(df)
df = df.drop_duplicates(subset=["ticker", "year", "context"]).reset_index(drop=True)
print(f"Dropped {before - len(df)} duplicate contexts")

print("Clean shape:", df.shape)
print("Unique tickers:", df["ticker"].nunique())
print("Years:", df["year"].value_counts().to_dict())
print("Context length (chars):")
print(df["context"].str.len().describe())
assert df["context"].notna().all() and df["ticker"].notna().all()
print(df.sample(5, random_state=0))
#  Saves the table in a data folder
os.makedirs("data/processed", exist_ok=True)
df.to_csv("data/processed/kaggle_clean.csv", index=False)
print("Saved data/processed/kaggle_clean.csv")