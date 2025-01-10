import pandas as pd

# Load the CSV file
file_path = "Stoke/dataset.csv"  # Replace with your CSV file path
df = pd.read_csv(file_path)

# Check for null values
print("Null values per column:")
print(df.isnull().sum())

# Check if any null values exist
if df.isnull().values.any():
    print("\nThere are null values in the dataset.")
else:
    print("\nNo null values found in the dataset.")

# Optional: Save a report of rows with null values
null_rows = df
