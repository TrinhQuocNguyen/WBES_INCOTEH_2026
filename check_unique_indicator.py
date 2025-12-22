import pandas as pd

# Load your file (using the merged result or the original)
df = pd.read_csv("vietnam_data_clean.csv")

# 1. Get the count of unique indicators
unique_count = df['indicator'].nunique()

# 2. Get the actual list of unique indicator names
unique_list = df['indicator'].unique()

print(f"Total number of unique indicators: {unique_count}")
print("-" * 30)
print("List of unique indicators:")
print(unique_list)
print("Count:")
print(len(unique_list))