# -*- coding: utf-8 -*-
"""RC and Descriptive statistics"""

import pandas as pd
import numpy as np

## Import file
from google.colab import files
uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

  df = pd.read_excel(fn)

display(df.head())


# Define Likert scale mapping (5-point)
likert_mapping = {
    'Strongly Disagree': 1,
    'Disagree': 2,
    'Neutral': 3,
    'Agree': 4,
    'Strongly Agree': 5
}

# Create numeric dataframe
df_numeric = df.copy()

# Question columns (1-77)
question_cols = [str(i) for i in range(1, 78)]

# Convert to numeric
for col in question_cols:
    df_numeric[col] = df_numeric[col].map(likert_mapping)

# Verify conversion
print(f"Conversion complete. Sample:")
print(df_numeric[question_cols[:5]].head())

df = df_numeric.copy()

reverse_coded_items = [
    '2', '5', '8', '10', '11', '13', '14',                    # 7 items
    '17', '19', '20', '21', '23', '24', '27', '33',           # 8 items
    '42', '43', '44', '49', '50', '51', '55', '57',           # 8 items
    '63', '65', '67', '68', '73', '75'                        # 6 items
]

df_r = df.copy()
for item in reverse_coded_items:
    df_r[item] = 6 - df_r[item]

df_r.head()

print(f"2 original: {df['2'].values[:3]}")
print(f"2 reversed: {df_r['2'].values[:3]}")
print(f"Sum (should be [6, 6, 6]): {(df['2'].values[:3] + df_r['2'].values[:3]).tolist()}")
print(f"df_r shape: {df_r.shape}")  # Should be (65, 77)
print(f"Missing values: {df_r.isnull().sum().sum()}")  # Should be 0

"""DESCRIPTIVE STATISTICS

"""

import pandas as pd
import numpy as np

# Define your 4 themes with ALL 77 items
themes = {
    'Technical Feasibility & Performance': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
    'Individual Acceptance': ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
    'Organizational Decision-Making': ['34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58'],
    'Business Models & Market Strategies': ['59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77']
}

# Create descriptive statistics table
descriptive_stats = []

for theme, items in themes.items():
    means = df_r[items].mean()

    mean_range = f"{means.min():.2f} - {means.max():.2f}"
    items_gte_4 = (means >= 4.00).sum()
    items_lt_3 = (means < 3.00).sum()
    avg_mean = means.mean()

    descriptive_stats.append({
        'Theme': theme,
        'Items': f"{items[0]}-{items[-1]}",
        'Mean Range': mean_range,
        'Items ≥ 4.00': items_gte_4,
        'Items < 3.00': items_lt_3,
        'Avg. Mean': f"{avg_mean:.2f}"
    })

# Create DataFrame and display
desc_stats_df = pd.DataFrame(descriptive_stats)
print(desc_stats_df.to_string(index=False))

import pandas as pd
import numpy as np

# Your 4 themes with correct item ranges (string format)
themes = {
    'Technical Feasibility &amp; Performance': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
    'Individual Acceptance': ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
    'Organizational Decision-Making': ['34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58'],
    'Business Models &amp; Market Strategies': ['59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77']
}

# Verify structure
for theme, items in themes.items():
    print(f"{theme}: {items[0]}-{items[-1]} ({len(items)} items)")

print(f"\nTotal items: {sum(len(items) for items in themes.values())}")

# ============================================================================
# 3. CRONBACH'S ALPHA CALCULATION
# ============================================================================
def cronbach_alpha(data):
    """Calculate Cronbach's Alpha"""
    n_items = data.shape[1]
    item_vars = data.var(axis=0, ddof=1)
    total_var = data.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - (item_vars.sum() / total_var))
    return alpha

reliability_results = []

for theme_name, items_list in themes.items(): # Changed (start, end) to items_list
    # The 'themes' dictionary now contains lists of item numbers (strings), not ranges.
    # So, theme_cols should be directly assigned from items_list.
    theme_cols = items_list # Use the items list directly
    theme_data = df_r[theme_cols]

    alpha = cronbach_alpha(theme_data)

    if alpha >= 0.9:
        interpretation = 'Excellent'
    elif alpha >= 0.8:
        interpretation = 'Good'
    elif alpha >= 0.7:
        interpretation = 'Acceptable'
    else:
        interpretation = 'Questionable'

    reliability_results.append({
        'Theme': theme_name,
        'N (Items)': len(theme_cols),
        'Cronbach Alpha': round(alpha, 3),
        'Interpretation': interpretation
    })

reliability_df = pd.DataFrame(reliability_results)

print("RELIABILITY ANALYSIS - CRONBACH'S ALPHA")
print("="*80)
print(reliability_df.to_string(index=False))
print()

# Save reliability analysis
reliability_df.to_excel('Reliability_Analysis_Cronbachs_Alpha.xlsx', index=False)
print("✓ Saved: Reliability_Analysis_Cronbachs_Alpha.xlsx")
print()

# ============================================================================
# 4. DESCRIPTIVE STATISTICS BY THEME
# ============================================================================
stats_results = []

for theme_name, items_list in themes.items(): # Changed (start, end) to items_list
    theme_cols = items_list # Use the items list directly
    theme_data = df_r[theme_cols]

    # Calculate statistics
    mean_val = theme_data.values.flatten().mean()
    std_val = theme_data.values.flatten().std(ddof=1)
    min_val = theme_data.min().min()
    max_val = theme_data.max().max()
    median_val = theme_data.values.flatten().flatten()
    median_val = np.median(median_val)

    # Count items >= 4.0 and < 3.0
    item_means = theme_data.mean(axis=0)
    items_above_4 = (item_means >= 4.0).sum()
    items_below_3 = (item_means < 3.0).sum()

    stats_results.append({
        'Theme': theme_name,
        'N (Items)': len(theme_cols),
        'N (Respondents)': len(theme_data),
        'Mean': round(mean_val, 2),
        'Std Dev': round(std_val, 2),
        'Median': round(median_val, 2),
        'Min': int(min_val),
        'Max': int(max_val),
        'Items >= 4.0': int(items_above_4),
        'Items < 3.0': int(items_below_3)
    })

stats_df = pd.DataFrame(stats_results)

print("DESCRIPTIVE STATISTICS BY THEME")
print("="*100)
print(stats_df.to_string(index=False))
print()

# Save descriptive statistics
stats_df.to_excel('Descriptive_Statistics_by_Theme.xlsx', index=False)
print("✓ Saved: Descriptive_Statistics_by_Theme.xlsx")
print()

# ============================================================================
# 5. ITEM-LEVEL STATISTICS
# ============================================================================
item_stats = []

for item_num in range(1, 78):
    col = str(item_num)
    item_data = df_r[col]

    # Determine which theme this item belongs to
    theme_name = None
    for theme, items_list in themes.items(): # Changed (start, end) to items_list
        # Check if the current item_num is present in the list of items for this theme
        if str(item_num) in items_list:
            theme_name = theme
            break

    # Check if reverse coded
    is_reverse = col in reverse_coded_items # Check if the string version of item_num is in reverse_coded_items

    item_stats.append({
        'Item': item_num,
        'Theme': theme_name,
        'Mean': round(item_data.mean(), 2),
        'Std Dev': round(item_data.std(ddof=1), 2),
        'Median': int(item_data.median()),
        'Min': int(item_data.min()),
        'Max': int(item_data.max()),
        'Reverse Coded': 'Yes' if is_reverse else 'No'
    })

item_stats_df = pd.DataFrame(item_stats)

print("ITEM-LEVEL STATISTICS (All 77 Items)")
print("="*100)
print(item_stats_df.to_string(index=False))
print()

# Save item-level statistics
item_stats_df.to_excel('Item_Level_Statistics.xlsx', index=False)
print("✓ Saved: Item_Level_Statistics.xlsx")
print()

print("="*100)
print("SUMMARY: All analyses completed successfully!")
print("="*100)

# ANALYSIS 1: ITEM DIAGNOSTICS
print("="*100)
print("ANALYSIS 1: ITEM DIAGNOSTICS REPORT")
print("="*100)

# Define question columns (1-77) and create a DataFrame with only these numeric columns
question_cols = [str(i) for i in range(1, 78)]
df_r_numeric_only = df_r[question_cols].copy()

def cronbach_alpha(data):
    n_items = data.shape[1]
    item_vars = data.var(axis=0, ddof=1)
    total_var = data.sum(axis=1).var(ddof=1)
    alpha = (n_items / (n_items - 1)) * (1 - (item_vars.sum() / total_var))
    return alpha

overall_alpha = cronbach_alpha(df_r_numeric_only)

item_diagnostics = []

for item_num in range(1, 78):
    col = str(item_num)
    item_data = df_r_numeric_only[col].values # Use numeric-only DataFrame

    # Item-Total Correlation
    total_score = df_r_numeric_only.sum(axis=1).values # Use numeric-only DataFrame for total score
    item_total_corr = np.corrcoef(item_data, total_score)[0, 1]

    # Alpha if item deleted
    cols_without_item = [str(i) for i in range(1, 78) if i != item_num]
    df_without_item = df_r_numeric_only[cols_without_item] # Use numeric-only DataFrame
    alpha_if_deleted = cronbach_alpha(df_without_item)

    alpha_change = alpha_if_deleted - overall_alpha

    # Item statistics
    item_mean = df_r_numeric_only[col].mean() # Use numeric-only DataFrame
    item_std = df_r_numeric_only[col].std(ddof=1) # Use numeric-only DataFrame

    # Rating
    if item_total_corr > 0.5 and alpha_change < 0:
        strength = 'Excellent'
        recommendation = 'KEEP - Strong contributor'
    elif item_total_corr > 0.35 and alpha_change < 0.02:
        strength = 'Good'
        recommendation = 'KEEP - Solid contributor'
    elif item_total_corr > 0.2:
        strength = 'Acceptable'
        recommendation = 'KEEP - Adequate contributor'
    elif item_total_corr > 0.1:
        strength = 'Weak'
        recommendation = 'FLAG - Consider removing'
    else:
        strength = 'Very Weak'
        recommendation = 'REMOVE - Problematic item'

    item_diagnostics.append({
        'Item': item_num,
        'Mean': round(item_mean, 2),
        'Std Dev': round(item_std, 2),
        'Item-Total Corr': round(item_total_corr, 3),
        'Alpha-if-Deleted': round(alpha_if_deleted, 3),
        'Alpha Change': round(alpha_change, 3),
        'Strength': strength,
        'Recommendation': recommendation,
        'Reverse Coded': 'Yes' if col in reverse_coded_items else 'No' # Check string for reverse_coded_items
    })

diagnostics_df = pd.DataFrame(item_diagnostics)
print(diagnostics_df.head(20).to_string(index=False))
print(f"\nOverall Cronbach's Alpha: {overall_alpha:.3f}")
print()

# Save Analysis 1
diagnostics_df.to_excel('Analysis_1_Item_Diagnostics.xlsx', index=False)
print("Saved: Analysis_1_Item_Diagnostics.xlsx")
print()

# ANALYSIS 2: INTER-ITEM CORRELATION MATRIX
print("="*100)
print("ANALYSIS 2: INTER-ITEM CORRELATION MATRIX")
print("="*100)

corr_matrix = df_r_numeric_only.corr() # Use numeric-only DataFrame
corr_matrix.to_excel('Analysis_2_Correlation_Matrix.xlsx')

# Find strong correlations
clusters_found = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if corr_matrix.iloc[i, j] > 0.5:
            item_i = int(corr_matrix.columns[i])
            item_j = int(corr_matrix.columns[j])
            corr_val = corr_matrix.iloc[i, j]
            clusters_found.append((item_i, item_j, corr_val))

print(f"Strong item clusters (r > 0.5): {len(clusters_found)}")
if len(clusters_found) > 0:
    print("Top 10 strong correlations:")
    for i, (item_i, item_j, corr_val) in enumerate(sorted(clusters_found, key=lambda x: x[2], reverse=True)[:10]):
        print(f"  Item {item_i} <--> Item {item_j}: r = {corr_val:.3f}")

# Create heatmap
import matplotlib.pyplot as plt
import seaborn as sns
plt.figure(figsize=(20, 18))
sns.heatmap(corr_matrix, cmap='coolwarm', center=0, vmin=-1, vmax=1,
            square=True, linewidths=0.5, cbar_kws={'label': 'Correlation'})
plt.title('Inter-Item Correlation Matrix (77x77)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('Analysis_2_Heatmap_Full.png', dpi=200, bbox_inches='tight')
plt.close()
print("\nSaved: Analysis_2_Heatmap_Full.png")
print("Saved: Analysis_2_Correlation_Matrix.xlsx")
print()

# ANALYSIS 3: EXPLORATORY FACTOR ANALYSIS
print("="*100)
print("ANALYSIS 3: EXPLORATORY FACTOR ANALYSIS (EFA)")
print("="*100)

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis

scaler = StandardScaler()
df_scaled = scaler.fit_transform(df_r_numeric_only) # Use numeric-only DataFrame

# Test different numbers of factors
factor_results = []
for n_factors in range(2, 16):
    try:
        fa = FactorAnalysis(n_components=n_factors, random_state=42, max_iter=500)
        fa.fit(df_scaled)
        explained_var = np.sum(fa.components_**2) / len(df_r_numeric_only.columns) # Use numeric-only DataFrame for column count
        factor_results.append({
            'n_factors': n_factors,
            'explained_variance': explained_var
        })
    except:
        pass

factor_results_df = pd.DataFrame(factor_results)

# Plot scree plot
plt.figure(figsize=(12, 6))
plt.plot(factor_results_df['n_factors'], factor_results_df['explained_variance'],
         marker='o', linewidth=2, markersize=8, color='darkblue')
plt.xlabel('Number of Factors', fontsize=12, fontweight='bold')
plt.ylabel('Cumulative Explained Variance', fontsize=12, fontweight='bold')
plt.title('Scree Plot: Optimal Number of Factors', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xticks(range(2, 16))
plt.tight_layout()
plt.savefig('Analysis_3_Scree_Plot.png', dpi=200, bbox_inches='tight')
plt.close()
print("Saved: Analysis_3_Scree_Plot.png")

optimal_n = 6
print(f"\nOptimal number of factors: {optimal_n}")
print(f"Explained variance: {factor_results_df[factor_results_df['n_factors']==optimal_n]['explained_variance'].values[0]:.3f}")

# Run EFA
fa_optimal = FactorAnalysis(n_components=optimal_n, random_state=42, max_iter=500)
factor_loadings = fa_optimal.fit_transform(df_scaled)

loadings_df = pd.DataFrame(
    fa_optimal.components_.T,
    columns=[f'Factor_{i+1}' for i in range(optimal_n)],
    index=[f'Item_{i}' for i in range(1, 78)]
)

loadings_df.to_excel('Analysis_3_Factor_Loadings.xlsx')
print("Saved: Analysis_3_Factor_Loadings.xlsx")
print()

# ANALYSIS 4: SUB-SCALE RELIABILITY
print("="*100)
print("ANALYSIS 4: SUB-SCALE RELIABILITY ANALYSIS")
print("="*100)

factor_items = {}
for factor_col in loadings_df.columns:
    items_in_factor = loadings_df[loadings_df[factor_col].abs() > 0.4].index.tolist()
    items_in_factor = [int(item.split('_')[1]) for item in items_in_factor]
    if len(items_in_factor) >= 3:
        factor_items[factor_col] = sorted(items_in_factor)

print(f"Identified {len(factor_items)} meaningful factors")
print()

subscale_results = []
for factor_name, items in factor_items.items():
    cols = [str(i) for i in items]
    subscale_data = df_r_numeric_only[cols] # Use numeric-only DataFrame
    alpha = cronbach_alpha(subscale_data)

    if alpha >= 0.8:
        interpretation = 'Excellent'
    elif alpha >= 0.7:
        interpretation = 'Good'
    elif alpha >= 0.65:
        interpretation = 'Acceptable'
    else:
        interpretation = 'Questionable'

    mean_loading = loadings_df.loc[[f'Item_{i}' for i in items], factor_name].abs().mean()

    subscale_results.append({
        'Factor': factor_name,
        'N Items': len(items),
        'Items': ', '.join([str(i) for i in items]),
        'Cronbach Alpha': round(alpha, 3),
        'Interpretation': interpretation,
        'Avg Loading': round(mean_loading, 3)
    })

    print(f"{factor_name}: {len(items)} items, Alpha = {alpha:.3f} ({interpretation})")

subscale_df = pd.DataFrame(subscale_results)
subscale_df.to_excel('Analysis_4_Subscale_Reliability.xlsx', index=False)
print("\nSaved: Analysis_4_Subscale_Reliability.xlsx")
print()

# ANALYSIS 5: ITEM STRENGTH RANKINGS
print("="*100)
print("ANALYSIS 5: ITEM STRENGTH RANKINGS")
print("="*100)

item_rankings = []

for item_num in range(1, 78):
    col = str(item_num)

    diag_row = diagnostics_df[diagnostics_df['Item'] == item_num].iloc[0]
    item_total_corr = diag_row['Item-Total Corr']
    alpha_change = diag_row['Alpha Change']
    strength = diag_row['Strength']

    # Average inter-item correlation
    other_cols = [str(i) for i in range(1, 78) if i != item_num]
    # Ensure we only correlate numeric columns from df_r_numeric_only
    item_corrs = corr_matrix.loc[col, other_cols]
    avg_item_corr = item_corrs.abs().mean()

    # Factor loading
    item_loadings = loadings_df.loc[f'Item_{item_num}'].abs()
    max_loading = item_loadings.max()
    primary_factor = item_loadings.idxmax()

    item_var = diag_row['Std Dev']

    # Overall score
    score = (item_total_corr * 0.4) + (max_loading * 0.4) + (avg_item_corr * 0.2)

    item_rankings.append({
        'Item': item_num,
        'Item-Total Corr': round(item_total_corr, 3),
        'Avg Inter-Item Corr': round(avg_item_corr, 3),
        'Primary Factor': primary_factor,
        'Max Loading': round(max_loading, 3),
        'Variance': round(item_var, 3),
        'Strength': strength,
        'Overall Score': round(score, 3)
    })

rankings_df = pd.DataFrame(item_rankings)
rankings_df = rankings_df.sort_values('Overall Score', ascending=False).reset_index(drop=True)
rankings_df['Rank'] = range(1, len(rankings_df) + 1)

rankings_df = rankings_df[['Rank', 'Item', 'Overall Score', 'Item-Total Corr',
                           'Avg Inter-Item Corr', 'Max Loading', 'Primary Factor',
                           'Variance', 'Strength']]

print("TOP 15 HIGHEST QUALITY ITEMS:")
print(rankings_df.head(15).to_string(index=False))
print()

rankings_df.to_excel('Analysis_5_Item_Rankings.xlsx', index=False)
print("Saved: Analysis_5_Item_Rankings.xlsx")
print()

# FINAL SUMMARY
print("="*100)
print("ANALYSIS SUMMARY")
print("="*100)
print()

excellent_items = len(rankings_df[rankings_df['Strength'] == 'Excellent'])
good_items = len(rankings_df[rankings_df['Strength'] == 'Good'])
acceptable_items = len(rankings_df[rankings_df['Strength'] == 'Acceptable'])
weak_items = len(rankings_df[rankings_df['Strength'].isin(['Weak', 'Very Weak'])])

print(f"1. Item Quality Distribution:")
print(f"   - Excellent: {excellent_items} items")
print(f"   - Good: {good_items} items")
print(f"   - Acceptable: {acceptable_items} items")
print(f"   - Weak/Very Weak: {weak_items} items")
print()

print(f"2. Factor Structure:")
print(f"   - Optimal factors: {optimal_n}")
print(f"   - Meaningful sub-scales: {len(factor_items)}")
print()

print(f"3. Publishable Sub-Scales (Alpha >= 0.65):")
publishable = subscale_df[subscale_df['Cronbach Alpha'] >= 0.65]
for idx, row in publishable.iterrows():
    print(f"   - {row['Factor']}: {row['N Items']} items, Alpha = {row['Cronbach Alpha']}")
print()

print(f"4. Strong Correlations (r > 0.5): {len(clusters_found)} pairs found")
print()

