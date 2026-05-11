import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "raw" / "DisasterDeclarationsSummaries.csv"

df = pd.read_csv(csv_path)

print("Rows and columns:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())
