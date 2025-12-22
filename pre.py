"""
Vietnam Enterprise Survey 2023 - Real Data Analysis
Analyzes actual data from World Bank Enterprise Survey
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Set style
plt.style.use('seaborn-whitegrid')
sns.set_palette("Set2")

def load_data(filepath='vietnam_data_clean.csv'):
    """Load the dataset"""
    print("=" * 70)
    print("LOADING DATA")
    print("=" * 70)
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        print(f"✓ Data loaded successfully")
        print(f"✓ Total records: {len(df):,}")
        print(f"✓ Total columns: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return None

def explore_data(df):
    """Explore the dataset structure"""
    print("\n" + "=" * 70)
    print("DATA EXPLORATION")
    print("=" * 70)
    
    print("\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print(f"\nData types:")
    print(df.dtypes)
    
    print(f"\nMissing values:")
    missing = df.isnull().sum()
    if missing.sum() > 0:
        print(missing[missing > 0])
    else:
        print("  No missing values")
    
    print(f"\nSample records:")
    print(df.head(3).to_string())
    
    return df

def analyze_indicators(df):
    """Analyze available indicators"""
    print("\n" + "=" * 70)
    print("INDICATOR ANALYSIS")
    print("=" * 70)
    
    # Unique indicators
    unique_indicators = df['indicator'].nunique()
    print(f"\n✓ Total unique indicators: {unique_indicators}")
    
    # English names
    unique_names = df['EnglishName'].nunique()
    print(f"✓ Total unique English names: {unique_names}")
    
    # Topics
    if 'Topic' in df.columns:
        unique_topics = df['Topic'].nunique()
        print(f"✓ Total unique topics: {unique_topics}")
        
        print("\nTop 15 Topics by record count:")
        topic_counts = df['Topic'].value_counts().head(15)
        for i, (topic, count) in enumerate(topic_counts.items(), 1):
            print(f"  {i:2d}. {topic[:60]:<60} {count:>6,} records")
    
    return df

def search_technology_indicators(df):
    """Search for technology-related indicators"""
    print("\n" + "=" * 70)
    print("TECHNOLOGY INDICATORS")
    print("=" * 70)
    
    tech_keywords = ['website', 'email', 'internet', 'computer', 'technology', 
                     'digital', 'online', 'software', 'broadband', 'ICT']
    
    tech_records = pd.DataFrame()
    
    for keyword in tech_keywords:
        matches = df[df['EnglishName'].str.contains(keyword, case=False, na=False)]
        if len(matches) > 0:
            print(f"\n'{keyword}' found in {len(matches)} records")
            unique_questions = matches['EnglishName'].unique()
            for q in unique_questions[:3]:  # Show first 3
                print(f"  - {q}")
            tech_records = pd.concat([tech_records, matches])
    
    tech_records = tech_records.drop_duplicates()
    print(f"\n✓ Total technology-related records: {len(tech_records)}")
    
    return tech_records

def search_innovation_indicators(df):
    """Search for innovation-related indicators"""
    print("\n" + "=" * 70)
    print("INNOVATION INDICATORS")
    print("=" * 70)
    
    innov_keywords = ['innovation', 'new product', 'new service', 'R&D', 'research',
                      'development', 'patent', 'license', 'upgrade', 'improve']
    
    innov_records = pd.DataFrame()
    
    for keyword in innov_keywords:
        matches = df[df['EnglishName'].str.contains(keyword, case=False, na=False)]
        if len(matches) > 0:
            print(f"\n'{keyword}' found in {len(matches)} records")
            unique_questions = matches['EnglishName'].unique()
            for q in unique_questions[:2]:
                print(f"  - {q}")
            innov_records = pd.concat([innov_records, matches])
    
    innov_records = innov_records.drop_duplicates()
    print(f"\n✓ Total innovation-related records: {len(innov_records)}")
    
    return innov_records

def search_performance_indicators(df):
    """Search for performance-related indicators"""
    print("\n" + "=" * 70)
    print("PERFORMANCE INDICATORS")
    print("=" * 70)
    
    perf_keywords = ['sales', 'productivity', 'growth', 'export', 'revenue',
                     'profit', 'performance', 'output', 'capacity']
    
    perf_records = pd.DataFrame()
    
    for keyword in perf_keywords:
        matches = df[df['EnglishName'].str.contains(keyword, case=False, na=False)]
        if len(matches) > 0:
            print(f"\n'{keyword}' found in {len(matches)} records")
            unique_questions = matches['EnglishName'].unique()
            for q in unique_questions[:2]:
                print(f"  - {q}")
            perf_records = pd.concat([perf_records, matches])
    
    perf_records = perf_records.drop_duplicates()
    print(f"\n✓ Total performance-related records: {len(perf_records)}")
    
    return perf_records

def search_firm_characteristics(df):
    """Search for firm characteristic indicators"""
    print("\n" + "=" * 70)
    print("FIRM CHARACTERISTICS")
    print("=" * 70)
    
    firm_keywords = ['size', 'age', 'small', 'medium', 'large', 'employees',
                     'sector', 'industry', 'ownership', 'location', 'establishment']
    
    firm_records = pd.DataFrame()
    
    for keyword in firm_keywords:
        matches = df[df['EnglishName'].str.contains(keyword, case=False, na=False)]
        if len(matches) > 0:
            print(f"\n'{keyword}' found in {len(matches)} records")
            unique_questions = matches['EnglishName'].unique()
            for q in unique_questions[:2]:
                print(f"  - {q}")
            firm_records = pd.concat([firm_records, matches])
    
    firm_records = firm_records.drop_duplicates()
    print(f"\n✓ Total firm characteristic records: {len(firm_records)}")
    
    return firm_records

def analyze_values(df):
    """Analyze the value distributions"""
    print("\n" + "=" * 70)
    print("VALUE ANALYSIS")
    print("=" * 70)
    
    # Check value column
    print(f"\nValue column data type: {df['value'].dtype}")
    print(f"Unique values count: {df['value'].nunique()}")
    
    # Sample values
    print("\nSample values:")
    print(df['value'].value_counts().head(20))
    
    # Try to identify numeric values
    numeric_mask = pd.to_numeric(df['value'], errors='coerce').notna()
    numeric_count = numeric_mask.sum()
    print(f"\n✓ Numeric values: {numeric_count:,} ({numeric_count/len(df)*100:.1f}%)")
    
    # Non-numeric values
    non_numeric = df[~numeric_mask]['value'].value_counts().head(10)
    print("\nTop non-numeric values:")
    for val, count in non_numeric.items():
        print(f"  '{val}': {count:,}")
    
    return df

def extract_useful_indicators(df):
    """Extract specific useful indicators for analysis"""
    print("\n" + "=" * 70)
    print("EXTRACTING KEY INDICATORS")
    print("=" * 70)
    
    results = {}
    
    # Technology adoption
    website_data = df[df['EnglishName'].str.contains('website', case=False, na=False)]
    if len(website_data) > 0:
        results['website'] = website_data
        print(f"✓ Website data: {len(website_data)} records")
    
    email_data = df[df['EnglishName'].str.contains('email|e-mail', case=False, na=False)]
    if len(email_data) > 0:
        results['email'] = email_data
        print(f"✓ Email data: {len(email_data)} records")
    
    # Firm size
    size_data = df[df['EnglishName'].str.contains('size|small|medium|large', case=False, na=False)]
    if len(size_data) > 0:
        results['firm_size'] = size_data
        print(f"✓ Firm size data: {len(size_data)} records")
    
    # Innovation
    innovation_data = df[df['EnglishName'].str.contains('innovat|new product|new service', case=False, na=False)]
    if len(innovation_data) > 0:
        results['innovation'] = innovation_data
        print(f"✓ Innovation data: {len(innovation_data)} records")
    
    return results

def create_summary_tables(df, tech_records, innov_records, perf_records, firm_records):
    """Create summary tables for the paper"""
    print("\n" + "=" * 70)
    print("CREATING SUMMARY TABLES")
    print("=" * 70)
    
    # Table 1: Data Overview
    print("\nTABLE 1: Dataset Overview")
    print("-" * 50)
    overview = pd.DataFrame({
        'Category': ['Total Records', 'Technology Indicators', 'Innovation Indicators', 
                    'Performance Indicators', 'Firm Characteristics', 'Unique Topics'],
        'Count': [len(df), len(tech_records), len(innov_records), 
                 len(perf_records), len(firm_records), df['Topic'].nunique()]
    })
    print(overview.to_string(index=False))
    
    # Table 2: Top Topics
    print("\n\nTABLE 2: Top 10 Topics by Coverage")
    print("-" * 50)
    top_topics = df['Topic'].value_counts().head(10).reset_index()
    top_topics.columns = ['Topic', 'Records']
    print(top_topics.to_string(index=False))
    
    return overview, top_topics

def create_visualizations(df, tech_records, innov_records):
    """Create visualizations"""
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Vietnam Enterprise Survey 2023 - Real Data Analysis', 
                 fontsize=16, fontweight='bold', y=0.995)
    
    # 1. Topic distribution
    ax1 = axes[0, 0]
    top_topics = df['Topic'].value_counts().head(10)
    top_topics.plot(kind='barh', ax=ax1, color='steelblue')
    ax1.set_xlabel('Number of Records')
    ax1.set_title('Top 10 Topics by Record Count')
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Indicator categories
    ax2 = axes[0, 1]
    categories = pd.DataFrame({
        'Category': ['Technology', 'Innovation', 'Performance', 'Firm Chars'],
        'Count': [len(tech_records), len(innov_records), 
                 len(df) - len(tech_records) - len(innov_records), 
                 len(df[df['EnglishName'].str.contains('size|age|sector', case=False, na=False)])]
    })
    ax2.bar(categories['Category'], categories['Count'], color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
    ax2.set_ylabel('Number of Records')
    ax2.set_title('Records by Indicator Category')
    ax2.tick_params(axis='x', rotation=45)
    ax2.grid(axis='y', alpha=0.3)
    
    # 3. Value type distribution
    ax3 = axes[1, 0]
    numeric_mask = pd.to_numeric(df['value'], errors='coerce').notna()
    value_types = pd.Series({
        'Numeric': numeric_mask.sum(),
        'Non-numeric': (~numeric_mask).sum()
    })
    ax3.pie(value_types, labels=value_types.index, autopct='%1.1f%%', 
            colors=['lightgreen', 'lightcoral'], startangle=90)
    ax3.set_title('Distribution of Value Types')
    
    # 4. Records by method
    ax4 = axes[1, 1]
    if 'method' in df.columns:
        method_counts = df['method'].value_counts().head(5)
        if len(method_counts) > 0:
            method_counts.plot(kind='bar', ax=ax4, color='mediumpurple')
            ax4.set_xlabel('Method')
            ax4.set_ylabel('Count')
            ax4.set_title('Top 5 Survey Methods')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('vietnam_real_data_analysis.png', dpi=300, bbox_inches='tight')
    print("✓ Visualization saved as 'vietnam_real_data_analysis.png'")
    
    return fig

def export_results(df, tech_records, innov_records, perf_records, firm_records):
    """Export analysis results"""
    print("\n" + "=" * 70)
    print("EXPORTING RESULTS")
    print("=" * 70)
    
    try:
        with pd.ExcelWriter('vietnam_real_analysis_results.xlsx', engine='openpyxl') as writer:
            # Overview
            overview = pd.DataFrame({
                'Metric': ['Total Records', 'Unique Indicators', 'Unique Topics',
                          'Technology Records', 'Innovation Records', 'Performance Records'],
                'Value': [len(df), df['indicator'].nunique(), df['Topic'].nunique(),
                         len(tech_records), len(innov_records), len(perf_records)]
            })
            overview.to_excel(writer, sheet_name='Overview', index=False)
            
            # Top topics
            top_topics = df['Topic'].value_counts().head(20).reset_index()
            top_topics.columns = ['Topic', 'Count']
            top_topics.to_excel(writer, sheet_name='Top Topics', index=False)
            
            # Technology indicators
            if len(tech_records) > 0:
                tech_summary = tech_records[['indicator', 'EnglishName', 'value']].drop_duplicates()
                tech_summary.to_excel(writer, sheet_name='Technology', index=False)
            
            # Innovation indicators
            if len(innov_records) > 0:
                innov_summary = innov_records[['indicator', 'EnglishName', 'value']].drop_duplicates()
                innov_summary.to_excel(writer, sheet_name='Innovation', index=False)
            
            # Sample data
            df.head(100).to_excel(writer, sheet_name='Sample Data', index=False)
        
        print("✓ Results exported to 'vietnam_real_analysis_results.xlsx'")
    except Exception as e:
        print(f"✗ Error exporting: {e}")

def main():
    """Main analysis workflow"""
    print("\n")
    print("=" * 70)
    print("  VIETNAM ENTERPRISE SURVEY 2023 - REAL DATA ANALYSIS")
    print("  World Bank Enterprise Survey - Comprehensive Analysis")
    print("=" * 70)
    
    # Load data
    df = load_data()
    if df is None:
        return
    
    # Explore structure
    df = explore_data(df)
    
    # Analyze indicators
    df = analyze_indicators(df)
    
    # Search specific categories
    tech_records = search_technology_indicators(df)
    innov_records = search_innovation_indicators(df)
    perf_records = search_performance_indicators(df)
    firm_records = search_firm_characteristics(df)
    
    # Analyze values
    df = analyze_values(df)
    
    # Extract key indicators
    results = extract_useful_indicators(df)
    
    # Create summary tables
    overview, top_topics = create_summary_tables(df, tech_records, innov_records, 
                                                  perf_records, firm_records)
    
    # Create visualizations
    create_visualizations(df, tech_records, innov_records)
    
    # Export results
    export_results(df, tech_records, innov_records, perf_records, firm_records)
    
    # Final summary
    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"\n✓ Total records analyzed: {len(df):,}")
    print(f"✓ Technology indicators: {len(tech_records):,}")
    print(f"✓ Innovation indicators: {len(innov_records):,}")
    print(f"✓ Performance indicators: {len(perf_records):,}")
    print(f"✓ Results exported to Excel")
    print(f"✓ Visualizations saved as PNG")
    
    print("\n" + "=" * 70)
    print("KEY FINDINGS FROM REAL DATA")
    print("=" * 70)
    print(f"1. Dataset contains {df['Topic'].nunique()} distinct topics")
    print(f"2. {len(tech_records)} records relate to technology adoption")
    print(f"3. {len(innov_records)} records relate to innovation activities")
    print(f"4. Top topic: {df['Topic'].value_counts().index[0]}")
    print(f"5. Survey methodology: {df['method'].value_counts().index[0] if 'method' in df.columns else 'N/A'}")
    
    print("\nFiles generated:")
    print("  - vietnam_real_data_analysis.png")
    print("  - vietnam_real_analysis_results.xlsx")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()