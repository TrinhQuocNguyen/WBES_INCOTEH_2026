import csv
import pandas as pd



# Convert from .dta to .csv
def convert_dta_to_csv(input_dta_file, output_csv_file):
    data = pd.read_stata(input_dta_file)
    data.to_csv(output_csv_file, index=False)
    print("✅ Converted .dta to .csv:", output_csv_file)

# Filter rows where "country" contains "viet nam2023"
def filter_country_contains_viet(input_file, output_file):
    with open(input_file, "r", encoding="latin1", errors="replace", newline="") as fin, \
         open(output_file, "w", encoding="utf-8", newline="") as fout:

        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=reader.fieldnames)

        # Write header
        writer.writeheader()

        for row in reader:
            country_value = row.get("country", "")
            if "viet nam2023" in country_value.lower():
                writer.writerow(row)

    print("✅ Filtered rows saved to:", output_file)

# Merge and clean data
def make_clean_file(input_file, indicator_file, output_file):

    # Load CSV files
    vietnam_df = pd.read_csv(input_file)
    indicator_df = pd.read_csv(indicator_file)

    # =========================
    # Clean key columns
    # - Remove ALL spaces from FieldName
    # - Remove ALL spaces from indicator too
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

    # Filter out specific indicators
    # Removes rows where indicator is "_sample" or "fieldworkdate"
    exclude_values = ["_sample", "fieldworkdate"]
    vietnam_df = vietnam_df[~vietnam_df["indicator"].isin(exclude_values)]

    # Select required columns
    indicator_df = indicator_df[["FieldName", "Topic", "EnglishName"]]

    # Merge datasets
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

    # Save output CSV
    merged_df.to_csv(output_file, index=False)

    print(f"✅ Clean File saved successfully: {output_file}")


if __name__ == "__main__":
    
    # Convert .dta to .csv
    FULL_DATA_CSV = "data/indicators_long_view_November_11_2024.csv"
    convert_dta_to_csv("data/indicators_long_view_November_11_2024.dta", 
                       FULL_DATA_CSV)
    
    # Filter for Vietnam 2023 only
    VIET2023_ONLY_FILE = "data/vietnam_2023_only.csv"
    filter_country_contains_viet(FULL_DATA_CSV, VIET2023_ONLY_FILE)
    
    # Make the final merged and cleaned file
    INDICATOR_FILE = "data/indicator_clean.csv"
    CLEAN_OUTPUT_FILE = "data/vietnam_data_clean.csv"
    make_clean_file(VIET2023_ONLY_FILE, INDICATOR_FILE, CLEAN_OUTPUT_FILE)

