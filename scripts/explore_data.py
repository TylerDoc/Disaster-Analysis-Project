import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "data" / "raw" / "DisasterDeclarationsSummaries.csv"

df = pd.read_csv(csv_path)

print("Rows and columns:", df.shape)

print("\nDisasters by state:")
print(df["state"].value_counts().head(15))

print("\nDisasters by incident type:")
print(df["incidentType"].value_counts())

print("\nDisasters by year:")
print(df["fyDeclared"].value_counts().sort_index())

print("\nDeclaration types:")
print(df["declarationType"].value_counts())

print("\nTop disaster titles:")
print(df["declarationTitle"].value_counts().head(15))
