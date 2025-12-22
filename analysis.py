import pandas as pd

# Load the CSV file 
df = pd.read_csv('vietnam_2023_modified.csv')

# Function to extract the value for a given indicator in a specific group
def get_value(cut, subcut, indicator):
    """
    Retrieve the 'value' column for the matching row.
    If cut/subcut are both 'All', look only at the overall rows.
    """
    if cut == 'All' and subcut == 'All':
        row = df[(df['cut'] == 'All') & (df['subcut'] == 'All') & (df['indicator'] == indicator)]
    else:
        row = df[(df['cut'] == cut) & (df['subcut'] == subcut) & (df['indicator'] == indicator)]
    
    if not row.empty:
        return row['value'].iloc[0]
    return None

# Overall statistics for the entire sample
overall_perf3 = get_value('All', 'All', 'perf3')
overall_comp1 = get_value('All', 'All', 'bready_comp1')
overall_comp4 = get_value('All', 'All', 'bready_comp4')
overall_comp7 = get_value('All', 'All', 'bready_comp7')
overall_comp8 = get_value('All', 'All', 'bready_comp8')
overall_in16 = get_value('All', 'All', 'in16')
overall_in9  = get_value('All', 'All', 'bready_in9')

print("Overall Statistics (All Enterprises):")
print(f"Labor Productivity Growth (perf3): {overall_perf3:.2f}%")
print(f"Workers Using Computers (bready_comp1): {overall_comp1:.2f}%")
print(f"Email Usage for Business (bready_comp4): {overall_comp4:.2f}%")
print(f"Website Ownership (bready_comp7): {overall_comp7:.2f}%")
print(f"High-Speed Internet Access (bready_comp8): {overall_comp8:.2f}%")
print(f"Investment in Fixed Assets (in16): {overall_in16:.2f}%")
print(f"Investment in R&D/Innovation (bready_in9): {overall_in9:.2f}%\n")

# Define the groups we want to compare
groups = {
    'Exporter (≥10% exports)': ('Exporter Type', 'Direct exports are 10% or more of sales'),
    'Non-exporter': ('Exporter Type', 'Non-exporter'),
    'Large (100+ employees)': ('Size', 'Large (100+)'),
    'Medium (20-99 employees)': ('Size', 'Medium (20-99)'),
    'Small (5-19 employees)': ('Size', 'Small (5-19)'),
}

# Indicators for the table (English column names)
indicators = {
    'Workers Using Computers (%)': 'bready_comp1',
    'Email Usage (%)': 'bready_comp4',
    'Website Ownership (%)': 'bready_comp7',
    'High-Speed Internet (%)': 'bready_comp8',
    'Fixed Assets Investment (%)': 'in16',
    'R&D Investment (%)': 'bready_in9',
    'Labor Productivity Growth (%)': 'perf3'
}

# Build table data
table_data = []
for group_name, (cut, subcut) in groups.items():
    row = [group_name]
    for col_name, ind_code in indicators.items():
        val = get_value(cut, subcut, ind_code)
        row.append(f"{val:.2f}" if val is not None else "N/A")
    table_data.append(row)

# Create DataFrame for nice printing
columns = ['Group'] + list(indicators.keys())
table_df = pd.DataFrame(table_data, columns=columns)

print("Table 1: Comparison of Technology Adoption and Labor Productivity by Enterprise Group")
print(table_df.to_string(index=False))

# Simple correlation across the selected groups (using the numerical values in the table)
numeric_df = table_df.iloc[:, 1:].apply(pd.to_numeric, errors='coerce')
if not numeric_df.empty:
    correlations = numeric_df.corr()['Labor Productivity Growth (%)'].drop('Labor Productivity Growth (%)')
    print("\nCorrelations with Labor Productivity Growth (across selected groups):")
    print(correlations.round(2))
else:
    print("\nNot enough numeric data to compute correlations.")