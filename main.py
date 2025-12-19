import csv

INPUT_FILE = "indicators_long_view_November_11_2024_converted.csv"
OUTPUT_FILE = "vietnam_2023_only.csv"

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


if __name__ == "__main__":
    filter_country_contains_viet(INPUT_FILE, OUTPUT_FILE)
