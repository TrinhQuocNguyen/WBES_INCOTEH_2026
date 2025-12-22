import pandas as pd

# Load the dataset
file_path = 'vietnam_data_clean.csv'
df = pd.read_csv(file_path)

# 1. Basic Dimensions
print("=== 1. DATASET OVERVIEW ===")
print(f"Total Observations (Rows): {df.shape[0]}")
print(f"Total Variables (Columns): {df.shape[1]}")
print(f"Columns: {', '.join(df.columns.tolist())}")

# 2. Scope of the Data
print("\n=== 2. SCOPE & CATEGORIES ===")
print(f"Unique Topics covered: {df['Topic'].nunique()}")
print(f"Unique Indicators:     {df['indicator'].nunique()}")
print(f"Disaggregation levels (Cuts): {df['cut'].unique().tolist()}")

# 3. Missing Data Check
print("\n=== 3. MISSING VALUES ===")
print(df.isnull().sum()[df.isnull().sum() > 0])

# 4. Numeric Summary (Value, SE, N)
# Ensure 'value' is numeric for the summary
df['value_numeric'] = pd.to_numeric(df['value'], errors='coerce')

print("\n=== 4. KEY METRICS SUMMARY ===")
summary_stats = df[['value_numeric', 'se', 'N']].describe().T
summary_stats = summary_stats[['count', 'mean', 'std', 'min', 'max']]
print(summary_stats)

# 5. Topic Breakdown (Useful for paper methodology)
print("\n=== 5. OBSERVATIONS BY TOPIC ===")
print(df['Topic'].value_counts())