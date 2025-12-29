import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the data
data = pd.read_csv('data/vietnam_data_clean.csv')

# Replace '.' with NaN and convert value, se, N to numeric
data['value'] = data['value'].replace('.', np.nan)
data['value'] = pd.to_numeric(data['value'], errors='coerce')
data['se'] = pd.to_numeric(data['se'], errors='coerce')
data['N'] = pd.to_numeric(data['N'], errors='coerce')

# Function to extract metrics for a group
def extract_metrics(df, indicators, cut='All', subcut='All'):
    filtered = df[(df['cut'] == cut) & (df['subcut'] == subcut) & (df['indicator'].isin(indicators))]
    return filtered[['indicator', 'value', 'se', 'N']]

# Indicators for Table 1: Innovation Metrics by Firm Size
inn_indicators = ['t5', 't7', 't9', 'bready_t1']
descriptions = {
    't5': 'Firms with own website',
    't7': 'New product/service in last 3 years',
    't9': 'Process innovation in last 3 years',
    'bready_t1': 'Quality certification'
}

# Extract for sizes
sizes = data[data['cut'] == 'Size']
small = sizes[sizes['subcut'] == 'Small (5-19)']
medium = sizes[sizes['subcut'] == 'Medium (20-99)']
large = sizes[sizes['subcut'] == 'Large (100+)']

small_inn = extract_metrics(small, inn_indicators, cut='Size', subcut='Small (5-19)')
medium_inn = extract_metrics(medium, inn_indicators, cut='Size', subcut='Medium (20-99)')
large_inn = extract_metrics(large, inn_indicators, cut='Size', subcut='Large (100+)')

# Print Table 1
print("Table 1. Innovation Metrics by Firm Size")
print("| Indicator | Description | Small (5-19) Value (%) | Medium (20-99) Value (%) | Large (100+) Value (%) |")
print("|-----------|-------------|------------------------|---------------------------|-------------------------|")

# Create DataFrame for Table 1 export
table1_data = []
for ind in inn_indicators:
    s_row = small_inn[small_inn['indicator'] == ind].iloc[0] if ind in small_inn['indicator'].values else pd.Series([np.nan]*4)
    m_row = medium_inn[medium_inn['indicator'] == ind].iloc[0] if ind in medium_inn['indicator'].values else pd.Series([np.nan]*4)
    l_row = large_inn[large_inn['indicator'] == ind].iloc[0] if ind in large_inn['indicator'].values else pd.Series([np.nan]*4)
    
    s_val = round(s_row['value'], 1) if not np.isnan(s_row['value']) else ''
    m_val = round(m_row['value'], 1) if not np.isnan(m_row['value']) else ''
    l_val = round(l_row['value'], 1) if not np.isnan(l_row['value']) else ''
    s_se = round(s_row['se'], 1) if not np.isnan(s_row['se']) else ''
    m_se = round(m_row['se'], 1) if not np.isnan(m_row['se']) else ''
    l_se = round(l_row['se'], 1) if not np.isnan(s_row['se']) else ''
    
    # Print to console
    print(f"| {ind} | {descriptions.get(ind, ind)} | {s_val} (se={s_se}, N={s_row['N']}) | {m_val} (se={m_se}, N={m_row['N']}) | {l_val} (se={l_se}, N={l_row['N']}) |")
    
    # Collect data for Excel export
    table1_data.append({
        'Indicator': ind,
        'Description': descriptions.get(ind, ind),
        'Small (5-19) Value (%)': s_val,
        'Small (5-19) SE': s_se,
        'Small (5-19) N': s_row['N'] if not np.isnan(s_row['N']) else '',
        'Medium (20-99) Value (%)': m_val,
        'Medium (20-99) SE': m_se,
        'Medium (20-99) N': m_row['N'] if not np.isnan(m_row['N']) else '',
        'Large (100+) Value (%)': l_val,
        'Large (100+) SE': l_se,
        'Large (100+) N': l_row['N'] if not np.isnan(l_row['N']) else ''
    })

# Create DataFrame for Table 1
table1_df = pd.DataFrame(table1_data)

# Export Table 1 to Excel
table1_df.to_excel('data/analyzed_results/Table1_Innovation_Metrics_by_Firm_Size.xlsx', index=False, sheet_name='Innovation Metrics')
print("\n ✅ Table 1 exported to: Table1_Innovation_Metrics_by_Firm_Size.xlsx")

# For correlations: We pivot to compute correlations across all available subgroups
# Collect all unique subcuts
all_groups = data[data['subcut'] != '']

# Indicators for correlation
corr_indicators = ['t5', 't7', 't9', 'perf1', 'perf2', 'perf3', 'bready_t1', 'fin14', 'bready_fin28', 'bready_fin31']

# Select and drop duplicates
filtered = all_groups[all_groups['indicator'].isin(corr_indicators)].drop_duplicates(subset=['cut', 'subcut', 'indicator'], keep='first')

# Pivot: subgroups as index, indicators as columns
pivoted = filtered.pivot(index=['cut', 'subcut'], columns='indicator', values='value').reset_index()

# Drop rows with all NaN in indicators
pivoted = pivoted.dropna(how='all', subset=corr_indicators)

pivoted.to_csv('data/Pivoted_Data.csv', index=False)
print("\n ✅ Pivoted data exported to: Pivoted_Data.csv")


# Compute correlation matrix
corr_matrix = pivoted[corr_indicators].corr().round(2)

# Fill NaN with 0 for display
corr_matrix = corr_matrix.fillna(0)

# Print Table 2
print("\nTable 2. Correlations Between Digital, Innovation, and Performance Indicators")
print(corr_matrix.to_string())

# Export Table 2 (Correlation Matrix) to Excel
corr_matrix.to_excel('Table2_Correlation_Matrix.xlsx', sheet_name='Correlations')
print("\nTable 2 exported to: Table2_Correlation_Matrix.xlsx")

# Create and save heatmap
fig, ax = plt.subplots(figsize=(10, 8))
im = ax.imshow(corr_matrix.values, cmap='coolwarm', vmin=-1, vmax=1)

# Labels
ax.set_xticks(np.arange(len(corr_matrix.columns)))
ax.set_yticks(np.arange(len(corr_matrix.columns)))
ax.set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
ax.set_yticklabels(corr_matrix.columns)

# Colorbar
plt.colorbar(im, ax=ax)

# Title
plt.title('Correlation Heatmap')

# Save to file
plt.savefig('figures/correlation_heatmap.png', dpi=300, bbox_inches='tight')
plt.close(fig)
print("\n✅ Correlation heatmap saved to: figures/correlation_heatmap.png")

# Optional: Export both tables to a single Excel file with multiple sheets
with pd.ExcelWriter('data/analyzed_results/Analysis_Results.xlsx', engine='openpyxl') as writer:
    table1_df.to_excel(writer, sheet_name='Table 1 - Innovation Metrics', index=False)
    corr_matrix.to_excel(writer, sheet_name='Table 2 - Correlations')
    
print("\n ✅ Both tables exported to single file: Analysis_Results.xlsx")
print("  - Sheet 1: Table 1 - Innovation Metrics")
print("  - Sheet 2: Table 2 - Correlations")