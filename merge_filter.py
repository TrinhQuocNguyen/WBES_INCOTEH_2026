import pandas as pd

# =========================
# File paths
# =========================
vietnam_file = "vietnam_2023_modified.csv"
indicator_file = "indicator_clean.csv"
output_file = "vietnam_data_clean.csv"

# =========================
# Load CSV files
# =========================
vietnam_df = pd.read_csv(vietnam_file)
indicator_df = pd.read_csv(indicator_file)

# =========================
# Clean key columns
# - Remove ALL spaces from FieldName
# - (Optional but recommended) remove spaces from indicator too
# =========================
indicator_df["FieldName"] = (
    indicator_df["FieldName"]
    .astype(str)
    .str.replace(" ", "", regex=False)
)

vietnam_df["indicator"] = (
    vietnam_df["indicator"]
    .astype(str)
    .str.replace(" ", "", regex=False)
)

# ============================================================
# NEW: Filter out specific indicators
# Removes rows where indicator is "_sample" or "fieldworkdate"
# ============================================================
exclude_values = ["_sample", "fieldworkdate"]
vietnam_df = vietnam_df[~vietnam_df["indicator"].isin(exclude_values)]

# =========================
# Select required columns
# =========================
indicator_df = indicator_df[["FieldName", "Topic", "EnglishName"]]

# =========================
# Merge datasets
# =========================
merged_df = vietnam_df.merge(
    indicator_df,
    how="left",
    left_on="indicator",
    right_on="FieldName"
)

# =========================
# Remove redundant column
# =========================
merged_df = merged_df.drop(columns=["FieldName"])

# =========================
# Reorder columns
# =========================
final_columns = [
    "country",
    "cabr",
    "year",
    "cut",
    "subcut",
    "indicator",
    "Topic",
    "EnglishName",
    "value",
    "se",
    "N",
    "method"
]

merged_df = merged_df[final_columns]

# =========================
# Save output CSV
# =========================
merged_df.to_csv(output_file, index=False)

print(f"File saved successfully: {output_file}")
