"""
Generate Figure 1: Distribution of Surveyed Firms by Size Category
For Section 3.1 Data Source
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
print("Loading data...")
data = pd.read_csv('vietnam_data_clean.csv')

# Replace '.' with NaN and convert to numeric
data['value'] = data['value'].replace('.', np.nan)
data['value'] = pd.to_numeric(data['value'], errors='coerce')
data['N'] = pd.to_numeric(data['N'], errors='coerce')

print(f"Dataset loaded: {len(data):,} records")
print(f"Unique indicators: {data['indicator'].nunique()}")

# Extract firm size distribution
# Get data where we have firm size breakdown
size_data = data[data['cut'] == 'Size'].copy()

# Get sample sizes for each size category from any indicator
# We'll use t5 (website) as it has complete data
size_distribution = size_data[size_data['indicator'] == 't5'][['subcut', 'N']].dropna()

if len(size_distribution) == 0:
    # If t5 doesn't work, try another common indicator
    for indicator in ['t7', 't9', 'bready_t1']:
        size_distribution = size_data[size_data['indicator'] == indicator][['subcut', 'N']].dropna()
        if len(size_distribution) > 0:
            break

# Create the data
size_categories = ['Small\n(5-19)', 'Medium\n(20-99)', 'Large\n(100+)']
firm_counts = [362, 375, 291]  # From Table 1 in the paper
total_firms = sum(firm_counts)
percentages = [(count/total_firms)*100 for count in firm_counts]

# Print summary statistics
print("\n" + "="*60)
print("DATASET SUMMARY")
print("="*60)
print(f"Total firms surveyed: {total_firms:,}")
print(f"\nFirm Distribution by Size:")
for cat, count, pct in zip(size_categories, firm_counts, percentages):
    print(f"  {cat.replace(chr(10), ' ')}: {count:>3} firms ({pct:>5.1f}%)")

# Create figure
fig, (ax2) = plt.subplots(1, 2, figsize=(14, 6))
fig.suptitle('Percentage Distribution of Surveyed Firms by Size Category', 
             fontsize=14, fontweight='bold', y=0.98)

# # Subplot 1: Bar chart
colors = ['#3498db', '#2ecc71', '#e74c3c']
# bars = ax1.bar(size_categories, firm_counts, color=colors, edgecolor='black', linewidth=1.5)
# ax1.set_ylabel('Number of Firms', fontsize=11)
# ax1.set_xlabel('Firm Size Category', fontsize=11)
# ax1.set_title('(a) Absolute Numbers', fontsize=11)
# ax1.grid(axis='y', alpha=0.3, linestyle='--')
# ax1.set_ylim(0, max(firm_counts) * 1.15)

# # Add value labels on bars
# for bar, count, pct in zip(bars, firm_counts, percentages):
#     height = bar.get_height()
#     ax1.text(bar.get_x() + bar.get_width()/2., height,
#              f'{count}\n({pct:.1f}%)',
#              ha='center', va='bottom', fontsize=10, fontweight='bold')

# Subplot 2: Pie chart
ax2.pie(firm_counts, labels=size_categories, autopct='%1.1f%%',
        colors=colors, startangle=90, textprops={'fontsize': 11},
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5})
# ax2.set_title('(b) Percentage Distribution', fontsize=11)

# Add summary text box
summary_text = (
    f"Total Sample: {total_firms:,} firms\n"
    f"Small firms: {firm_counts[0]} ({percentages[0]:.1f}%)\n"
    f"Medium firms: {firm_counts[1]} ({percentages[1]:.1f}%)\n"
    f"Large firms: {firm_counts[2]} ({percentages[2]:.1f}%)"
)

fig.text(0.5, 0.02, summary_text, ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout(rect=[0, 0.06, 1, 0.96])
plt.savefig('figure1_firm_distribution.png', dpi=300, bbox_inches='tight')
print("\n✓ Figure saved as 'figure1_firm_distribution.png'")
plt.show()

# Additional dataset statistics
print("\n" + "="*60)
print("ADDITIONAL DATASET INFORMATION")
print("="*60)

# Check for unique cuts (categories)
print(f"\nCategory types (cut) in dataset:")
for cut in data['cut'].unique():
    count = len(data[data['cut'] == cut])
    print(f"  - {cut}: {count:,} records")

# Check for topics covered
if 'Topic' in data.columns:
    print(f"\nNumber of topics covered: {data['Topic'].nunique()}")
    print("\nTop 5 topics by record count:")
    top_topics = data['Topic'].value_counts().head(5)
    for i, (topic, count) in enumerate(top_topics.items(), 1):
        print(f"  {i}. {topic[:50]}: {count:,} records")

# Sample of key indicators
print("\nKey indicators used in analysis:")
key_indicators = ['t5', 't7', 't9', 'perf1', 'perf2', 'perf3', 
                  'bready_t1', 'fin14', 'bready_fin28', 'bready_fin31']
for ind in key_indicators:
    ind_data = data[data['indicator'] == ind]
    if len(ind_data) > 0:
        # Get the description from EnglishName if available
        if 'EnglishName' in data.columns:
            desc = ind_data['EnglishName'].iloc[0] if len(ind_data) > 0 else ''
            print(f"  {ind}: {desc[:60]}")
        else:
            print(f"  {ind}: {len(ind_data)} records")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
print("\nOutput files:")
print("  - figure1_firm_distribution.png (for paper)")
print("\nThis figure can be inserted into Section 3.1 of the paper.")