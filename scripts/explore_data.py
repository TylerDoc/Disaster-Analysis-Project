# Import libraries needed for reading the CSV file and handling file paths
import pandas as pd
from pathlib import Path

# Set the project root folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Set the file path for the raw FEMA disaster data
csv_path = BASE_DIR / "data" / "raw" / "DisasterDeclarationsSummaries.csv"

# Read the FEMA CSV file into a pandas DataFrame
df = pd.read_csv(csv_path)

# Display the total number of rows and columns in the dataset
print("Rows and columns:", df.shape)

# Show the top 15 states or jurisdictions with the most disaster declarations
print("\nDisasters by state:")
print(df["state"].value_counts().head(15))

# Show how many records exist for each disaster incident type
print("\nDisasters by incident type:")
print(df["incidentType"].value_counts())

# Show the number of disaster declarations by fiscal year
print("\nDisasters by year:")
print(df["fyDeclared"].value_counts().sort_index())

# Show the count for each FEMA declaration type
print("\nDeclaration types:")
print(df["declarationType"].value_counts())

# Show the most common disaster declaration titles
print("\nTop disaster titles:")
print(df["declarationTitle"].value_counts().head(15))
