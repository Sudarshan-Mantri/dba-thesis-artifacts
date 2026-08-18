# -*- coding: utf-8 -*-
"""3. Reliability, Normality & Correlation"""

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

df_numeric.head()

df = df_numeric.copy()

# ============================================================================
# CRONBACH'S ALPHA CALCULATION - THEME LEVEL ONLY
# ============================================================================

def cronbach_alpha(df, items):
    """
    Calculate Cronbach's Alpha for a set of items

    Parameters:
    df: DataFrame containing the item responses
    items: List of column names (item identifiers)

    Returns:
    alpha: Cronbach's Alpha coefficient
    """
    # Select only the specified items and remove any rows with missing values
    item_data = df[items].dropna()

    # Number of items
    k = len(items)

    # Calculate variance of each item
    item_variances = item_data.var(axis=0, ddof=1)

    # Calculate total score for each respondent
    total_scores = item_data.sum(axis=1)

    # Calculate variance of total scores
    total_variance = total_scores.var(ddof=1)

    # Calculate Cronbach's Alpha
    alpha = (k / (k - 1)) * (1 - (item_variances.sum() / total_variance))

    return alpha

def interpret_alpha(alpha):
    """
    Provide interpretation of Cronbach's Alpha value

    Parameters:
    alpha: Cronbach's Alpha coefficient

    Returns:
    interpretation: String describing the reliability level
    """
    if alpha >= 0.90:
        return "Excellent"
    elif alpha >= 0.80:
        return "Good"
    elif alpha >= 0.70:
        return "Acceptable"
    elif alpha >= 0.60:
        return "Questionable"
    elif alpha >= 0.50:
        return "Poor"
    else:
        return "Unacceptable"

# ============================================================================
# DEFINE THE 4 MAIN THEMES
# ============================================================================

main_themes = {
    'Theme 1: Technical Feasibility and Performance': {
        'items': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
        'description': 'Technical capabilities, performance metrics, security, and regulatory compliance'
    },
    'Theme 2: Individual Acceptance': {
        'items': ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
        'description': 'Trust, confidence, change resistance, user training, and proficiency'
    },
    'Theme 3: Organizational Decision Making': {
        'items': ['34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58'],
        'description': 'Leadership alignment, ROI, budgeting, pilot testing, phased rollout, and operational risk'
    },
    'Theme 4: Business Models and Market Strategies': {
        'items': ['59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77'],
        'description': 'Value proposition, market drivers, vendor partnerships, and pricing models'
    }
}

# ============================================================================
# CALCULATE RELIABILITY FOR EACH THEME
# ============================================================================

print("="*80)
print("RELIABILITY ANALYSIS: MAIN THEMES")
print("="*80)
print(f"\nSample Size: {len(df)} respondents")
print(f"Number of Themes: {len(main_themes)}")
print(f"Total Items: 77 questions (Q1-Q77)")
print("\n")

# Store results
reliability_results = []

for theme_name, theme_info in main_themes.items():
    items = theme_info['items']
    description = theme_info['description']

    # Calculate Cronbach's Alpha
    alpha = cronbach_alpha(df, items)
    interpretation = interpret_alpha(alpha)

    # Store results
    reliability_results.append({
        'Theme': theme_name,
        'Number of Items': len(items),
        'Item Range': f"Q{items[0]} to Q{items[-1]}",
        'Cronbach Alpha': round(alpha, 4),
        'Interpretation': interpretation,
        'Description': description
    })

    # Print individual theme results
    print(f"{theme_name}")
    print("-" * 80)
    print(f"  Items: {len(items)} questions (Q{items[0]} to Q{items[-1]})")
    print(f"  Description: {description}")
    print(f"  Cronbach's Alpha: {alpha:.4f}")
    print(f"  Interpretation: {interpretation}")
    print("\n")

# ============================================================================
# CREATE SUMMARY TABLE
# ============================================================================

reliability_df = pd.DataFrame(reliability_results)

print("="*80)
print("SUMMARY TABLE: THEME-LEVEL RELIABILITY")
print("="*80)
print("\n")
print(reliability_df[['Theme', 'Number of Items', 'Cronbach Alpha', 'Interpretation']].to_string(index=False))
print("\n")

# ============================================================================
# ADDITIONAL STATISTICS
# ============================================================================

print("="*80)
print("RELIABILITY STATISTICS SUMMARY")
print("="*80)
print(f"\nMean Cronbach's Alpha across all themes: {reliability_df['Cronbach Alpha'].mean():.4f}")
print(f"Median Cronbach's Alpha: {reliability_df['Cronbach Alpha'].median():.4f}")
print(f"Minimum Cronbach's Alpha: {reliability_df['Cronbach Alpha'].min():.4f}")
print(f"Maximum Cronbach's Alpha: {reliability_df['Cronbach Alpha'].max():.4f}")
print(f"Standard Deviation: {reliability_df['Cronbach Alpha'].std():.4f}")

# Count by interpretation category
print("\n" + "="*80)
print("RELIABILITY DISTRIBUTION")
print("="*80)
interpretation_counts = reliability_df['Interpretation'].value_counts()
for interp, count in interpretation_counts.items():
    percentage = (count / len(reliability_df)) * 100
    print(f"{interp}: {count} theme(s) ({percentage:.1f}%)")

# ============================================================================
# SAVE RESULTS TO EXCEL
# ============================================================================

# Save to Excel file
output_file = '/content/Theme_Reliability_Analysis.xlsx'
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    reliability_df.to_excel(writer, sheet_name='Theme Reliability', index=False)

print(f"\n✓ Results saved to: {output_file}")
print("="*80)

import pandas as pd
import numpy as np
from scipy import stats
from scipy.stats import shapiro, normaltest, pearsonr, spearmanr
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# PART 1: CALCULATE THEME SCORES
# ============================================================================

print("="*80)
print("THEME-WISE NORMALITY TESTING & CORRELATION ANALYSIS")
print("="*80)
print("\n")

# Define the 4 main themes
theme_definitions = {
    'Theme1_Technical': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14'],
    'Theme2_Individual': ['15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33'],
    'Theme3_Organizational': ['34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58'],
    'Theme4_Business': ['59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77']
}

# Calculate mean scores for each theme
print("Calculating theme scores (mean of items in each theme)...")
print("-" * 80)

for theme_name, items in theme_definitions.items():
    df[theme_name] = df[items].mean(axis=1)
    print(f"{theme_name}: Mean of {len(items)} items (Q{items[0]}-Q{items[-1]})")

print("\n✓ Theme scores calculated successfully!\n")

# Create a dataframe with just the theme scores
theme_scores = df[['Theme1_Technical', 'Theme2_Individual', 'Theme3_Organizational', 'Theme4_Business']]

print(f"Sample size: {len(theme_scores)} respondents")
print(f"Number of themes: {len(theme_scores.columns)}")
print("\n")

# ============================================================================
# PART 2: DESCRIPTIVE STATISTICS FOR THEMES
# ============================================================================

print("="*80)
print("DESCRIPTIVE STATISTICS - THEME SCORES")
print("="*80)
print("\n")

descriptive_stats = pd.DataFrame({
    'Theme': [
        'Theme 1: Technical Feasibility',
        'Theme 2: Individual Acceptance',
        'Theme 3: Organizational Decision Making',
        'Theme 4: Business Models'
    ],
    'Mean': [
        theme_scores['Theme1_Technical'].mean(),
        theme_scores['Theme2_Individual'].mean(),
        theme_scores['Theme3_Organizational'].mean(),
        theme_scores['Theme4_Business'].mean()
    ],
    'Median': [
        theme_scores['Theme1_Technical'].median(),
        theme_scores['Theme2_Individual'].median(),
        theme_scores['Theme3_Organizational'].median(),
        theme_scores['Theme4_Business'].median()
    ],
    'SD': [
        theme_scores['Theme1_Technical'].std(),
        theme_scores['Theme2_Individual'].std(),
        theme_scores['Theme3_Organizational'].std(),
        theme_scores['Theme4_Business'].std()
    ],
    'Min': [
        theme_scores['Theme1_Technical'].min(),
        theme_scores['Theme2_Individual'].min(),
        theme_scores['Theme3_Organizational'].min(),
        theme_scores['Theme4_Business'].min()
    ],
    'Max': [
        theme_scores['Theme1_Technical'].max(),
        theme_scores['Theme2_Individual'].max(),
        theme_scores['Theme3_Organizational'].max(),
        theme_scores['Theme4_Business'].max()
    ],
    'Skewness': [
        theme_scores['Theme1_Technical'].skew(),
        theme_scores['Theme2_Individual'].skew(),
        theme_scores['Theme3_Organizational'].skew(),
        theme_scores['Theme4_Business'].skew()
    ],
    'Kurtosis': [
        theme_scores['Theme1_Technical'].kurtosis(),
        theme_scores['Theme2_Individual'].kurtosis(),
        theme_scores['Theme3_Organizational'].kurtosis(),
        theme_scores['Theme4_Business'].kurtosis()
    ]
})

# Round to 3 decimal places
descriptive_stats[['Mean', 'Median', 'SD', 'Min', 'Max', 'Skewness', 'Kurtosis']] = \
    descriptive_stats[['Mean', 'Median', 'SD', 'Min', 'Max', 'Skewness', 'Kurtosis']].round(3)

print(descriptive_stats.to_string(index=False))
print("\n")

# ============================================================================
# PART 3: NORMALITY TESTING
# ============================================================================

print("="*80)
print("NORMALITY TESTING - SHAPIRO-WILK TEST")
print("="*80)
print("\n")

normality_results = []

theme_labels = {
    'Theme1_Technical': 'Theme 1: Technical Feasibility and Performance',
    'Theme2_Individual': 'Theme 2: Individual Acceptance',
    'Theme3_Organizational': 'Theme 3: Organizational Decision Making',
    'Theme4_Business': 'Theme 4: Business Models and Market Strategies'
}

for theme_col, theme_label in theme_labels.items():
    # Shapiro-Wilk test
    statistic, p_value = shapiro(theme_scores[theme_col].dropna())

    # Interpretation
    if p_value > 0.05:
        interpretation = "Normal distribution (p > 0.05)"
        normality = "Yes"
    else:
        interpretation = "Non-normal distribution (p ≤ 0.05)"
        normality = "No"

    normality_results.append({
        'Theme': theme_label,
        'Shapiro-Wilk Statistic': round(statistic, 4),
        'p-value': round(p_value, 4),
        'Normal Distribution?': normality,
        'Interpretation': interpretation
    })

    print(f"{theme_label}")
    print("-" * 80)
    print(f"  Shapiro-Wilk Statistic: {statistic:.4f}")
    print(f"  p-value: {p_value:.4f}")
    print(f"  Interpretation: {interpretation}")
    print("\n")

normality_df = pd.DataFrame(normality_results)

print("="*80)
print("NORMALITY TEST SUMMARY")
print("="*80)
print("\n")
print(normality_df[['Theme', 'Shapiro-Wilk Statistic', 'p-value', 'Normal Distribution?']].to_string(index=False))
print("\n")

# Count normal vs non-normal
normal_count = normality_df['Normal Distribution?'].value_counts()
print(f"Themes with normal distribution: {normal_count.get('Yes', 0)} of 4")
print(f"Themes with non-normal distribution: {normal_count.get('No', 0)} of 4")
print("\n")

# ============================================================================
# PART 4: VISUAL ASSESSMENT OF NORMALITY
# ============================================================================

print("="*80)
print("CREATING NORMALITY VISUALIZATIONS")
print("="*80)
print("\n")

# Create figure with histograms and Q-Q plots
fig, axes = plt.subplots(4, 2, figsize=(14, 16))
fig.suptitle('Normality Assessment: Histograms and Q-Q Plots', fontsize=16, fontweight='bold', y=0.995)

theme_names_short = ['Theme 1: Technical', 'Theme 2: Individual', 'Theme 3: Organizational', 'Theme 4: Business']

for idx, (theme_col, theme_name) in enumerate(zip(theme_scores.columns, theme_names_short)):
    # Histogram
    axes[idx, 0].hist(theme_scores[theme_col].dropna(), bins=15, color='steelblue',
                      edgecolor='black', alpha=0.7)
    axes[idx, 0].axvline(theme_scores[theme_col].mean(), color='red',
                         linestyle='--', linewidth=2, label=f'Mean = {theme_scores[theme_col].mean():.2f}')
    axes[idx, 0].axvline(theme_scores[theme_col].median(), color='green',
                         linestyle='--', linewidth=2, label=f'Median = {theme_scores[theme_col].median():.2f}')
    axes[idx, 0].set_xlabel('Theme Score', fontsize=10)
    axes[idx, 0].set_ylabel('Frequency', fontsize=10)
    axes[idx, 0].set_title(f'{theme_name} - Distribution', fontsize=11, fontweight='bold')
    axes[idx, 0].legend(fontsize=9)
    axes[idx, 0].grid(axis='y', alpha=0.3)

    # Q-Q Plot
    stats.probplot(theme_scores[theme_col].dropna(), dist="norm", plot=axes[idx, 1])
    axes[idx, 1].set_title(f'{theme_name} - Q-Q Plot', fontsize=11, fontweight='bold')
    axes[idx, 1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/content/Normality_Assessment.png', dpi=300, bbox_inches='tight')
print("✓ Normality visualizations saved: Normality_Assessment.png")
print("\n")

# ============================================================================
# PART 5: CORRELATION ANALYSIS - PEARSON
# ============================================================================

print("="*80)
print("CORRELATION ANALYSIS - PEARSON CORRELATION")
print("="*80)
print("\n")

# Calculate Pearson correlation matrix
pearson_corr = theme_scores.corr(method='pearson')

# Calculate p-values for correlations
def calculate_pvalues(df):
    """Calculate p-values for Pearson correlation"""
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(pearsonr(df[r], df[c])[1], 4)
    return pvalues

pearson_pvalues = calculate_pvalues(theme_scores)

print("PEARSON CORRELATION MATRIX")
print("-" * 80)
print("\nCorrelation Coefficients:")
print(pearson_corr.round(3).to_string())
print("\n")
print("P-values:")
print(pearson_pvalues.to_string())
print("\n")

# Create detailed correlation table
correlation_pairs = []
themes = ['Theme1_Technical', 'Theme2_Individual', 'Theme3_Organizational', 'Theme4_Business']
theme_names_full = [
    'Theme 1: Technical Feasibility',
    'Theme 2: Individual Acceptance',
    'Theme 3: Organizational Decision Making',
    'Theme 4: Business Models'
]

for i in range(len(themes)):
    for j in range(i+1, len(themes)):
        r_value = pearson_corr.loc[themes[i], themes[j]]
        p_value = float(pearson_pvalues.loc[themes[i], themes[j]])

        # Determine significance
        if p_value < 0.001:
            sig = '***'
            sig_text = 'p < 0.001'
        elif p_value < 0.01:
            sig = '**'
            sig_text = 'p < 0.01'
        elif p_value < 0.05:
            sig = '*'
            sig_text = 'p < 0.05'
        else:
            sig = 'ns'
            sig_text = 'p ≥ 0.05 (not significant)'

        # Interpret strength
        abs_r = abs(r_value)
        if abs_r >= 0.70:
            strength = 'Strong'
        elif abs_r >= 0.40:
            strength = 'Moderate'
        elif abs_r >= 0.20:
            strength = 'Weak'
        else:
            strength = 'Very Weak'

        correlation_pairs.append({
            'Theme Pair': f"{theme_names_full[i]} ↔ {theme_names_full[j]}",
            'r': round(r_value, 3),
            'p-value': round(p_value, 4),
            'Significance': sig,
            'Strength': strength,
            'Interpretation': f"{strength} {('positive' if r_value > 0 else 'negative')} correlation ({sig_text})"
        })

correlation_df = pd.DataFrame(correlation_pairs)

print("="*80)
print("DETAILED CORRELATION RESULTS")
print("="*80)
print("\n")
print(correlation_df[['Theme Pair', 'r', 'p-value', 'Significance', 'Strength']].to_string(index=False))
print("\n")
print("Significance levels: *** p<0.001, ** p<0.01, * p<0.05, ns = not significant")
print("\n")

# ============================================================================
# PART 6: CORRELATION ANALYSIS - SPEARMAN (NON-PARAMETRIC)
# ============================================================================

print("="*80)
print("CORRELATION ANALYSIS - SPEARMAN CORRELATION (NON-PARAMETRIC)")
print("="*80)
print("\n")

# Calculate Spearman correlation matrix
spearman_corr = theme_scores.corr(method='spearman')

# Calculate p-values for Spearman correlations
def calculate_spearman_pvalues(df):
    """Calculate p-values for Spearman correlation"""
    dfcols = pd.DataFrame(columns=df.columns)
    pvalues = dfcols.transpose().join(dfcols, how='outer')
    for r in df.columns:
        for c in df.columns:
            pvalues[r][c] = round(spearmanr(df[r], df[c])[1], 4)
    return pvalues

spearman_pvalues = calculate_spearman_pvalues(theme_scores)

print("SPEARMAN CORRELATION MATRIX")
print("-" * 80)
print("\nCorrelation Coefficients:")
print(spearman_corr.round(3).to_string())
print("\n")
print("P-values:")
print(spearman_pvalues.to_string())
print("\n")

# ============================================================================
# PART 7: CORRELATION VISUALIZATION
# ============================================================================

print("="*80)
print("CREATING CORRELATION VISUALIZATIONS")
print("="*80)
print("\n")

# Create correlation heatmap
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Pearson correlation heatmap
theme_labels_short = ['Technical\nFeasibility', 'Individual\nAcceptance',
                      'Organizational\nDecision Making', 'Business\nModels']

sns.heatmap(pearson_corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            vmin=-1, vmax=1, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            xticklabels=theme_labels_short, yticklabels=theme_labels_short, ax=ax1)
ax1.set_title('Pearson Correlation Matrix\n(Parametric)', fontsize=13, fontweight='bold', pad=15)

# Spearman correlation heatmap
sns.heatmap(spearman_corr, annot=True, fmt='.3f', cmap='coolwarm', center=0,
            vmin=-1, vmax=1, square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            xticklabels=theme_labels_short, yticklabels=theme_labels_short, ax=ax2)
ax2.set_title('Spearman Correlation Matrix\n(Non-Parametric)', fontsize=13, fontweight='bold', pad=15)

plt.tight_layout()
plt.savefig('/content/Correlation_Heatmaps.png', dpi=300, bbox_inches='tight')
print("✓ Correlation heatmaps saved: Correlation_Heatmaps.png")
print("\n")

# Create scatter plot matrix
fig = plt.figure(figsize=(16, 16))
fig.suptitle('Scatter Plot Matrix: Theme-wise Correlations', fontsize=16, fontweight='bold', y=0.995)

plot_idx = 1
for i in range(4):
    for j in range(4):
        ax = plt.subplot(4, 4, plot_idx)

        if i == j:
            # Diagonal: histogram
            ax.hist(theme_scores.iloc[:, i].dropna(), bins=15, color='steelblue',
                   edgecolor='black', alpha=0.7)
            ax.set_ylabel('Frequency', fontsize=9)
        else:
            # Off-diagonal: scatter plot
            ax.scatter(theme_scores.iloc[:, j],
                          theme_scores.iloc[:, i],
                          alpha=0.6, s=50, color='steelblue', edgecolors='black', linewidth=0.5)

            # Add regression line
            z = np.polyfit(theme_scores.iloc[:, j].dropna(),
                          theme_scores.iloc[:, i].dropna(), 1)
            p = np.poly1d(z)
            ax.plot(theme_scores.iloc[:, j].sort_values(),
                   p(theme_scores.iloc[:, j].sort_values()),
                   "r--", linewidth=2, alpha=0.8)

            # Add correlation coefficient
            r_val = pearson_corr.iloc[i, j]
            ax.text(0.05, 0.95, f'r = {r_val:.3f}',
                   transform=ax.transAxes, fontsize=10,
                   verticalalignment='top', fontweight='bold',
                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        # Labels
        if i == 3:
            ax.set_xlabel(theme_names_short[j], fontsize=10, fontweight='bold')
        if j == 0:
            ax.set_ylabel(theme_names_short[i], fontsize=10, fontweight='bold')

        ax.grid(alpha=0.3)
        plot_idx += 1

plt.tight_layout()
plt.savefig('/content/Scatter_Plot_Matrix.png', dpi=300, bbox_inches='tight')
print("✓ Scatter plot matrix saved: Scatter_Plot_Matrix.png")
print("\n")

# ============================================================================
# PART 8: SUMMARY STATISTICS
# ============================================================================

print("="*80)
print("SUMMARY STATISTICS")
print("="*80)
print("\n")

print("CORRELATION STRENGTH DISTRIBUTION:")
print("-" * 80)
strength_counts = correlation_df['Strength'].value_counts()
for strength, count in strength_counts.items():
    percentage = (count / len(correlation_df)) * 100
    print(f"{strength}: {count} pair(s) ({percentage:.1f}%)")

print("\n")
print("CORRELATION SIGNIFICANCE DISTRIBUTION:")
print("-" * 80)
sig_counts = correlation_df['Significance'].value_counts()
sig_labels = {'***': 'Highly significant (p < 0.001)',
              '**': 'Very significant (p < 0.01)',
              '*': 'Significant (p < 0.05)',
              'ns': 'Not significant (p ≥ 0.05)'}
for sig, count in sig_counts.items():
    percentage = (count / len(correlation_df)) * 100
    print(f"{sig_labels.get(sig, sig)}: {count} pair(s) ({percentage:.1f}%)")

print("\n")
print("STRONGEST CORRELATIONS:")
print("-" * 80)
strongest = correlation_df.nlargest(3, 'r')[['Theme Pair', 'r', 'Significance', 'Strength']]
print(strongest.to_string(index=False))

print("\n")
print("WEAKEST CORRELATIONS:")
print("-" * 80)
weakest = correlation_df.nsmallest(3, 'r')[['Theme Pair', 'r', 'Significance', 'Strength']]
print(weakest.to_string(index=False))

print("\n")

# ============================================================================
# PART 9: SAVE RESULTS TO EXCEL
# ============================================================================

print("="*80)
print("SAVING RESULTS TO EXCEL")
print("="*80)
print("\n")

output_file = '/content/Normality_Correlation_Analysis.xlsx'

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    # Sheet 1: Descriptive Statistics
    descriptive_stats.to_excel(writer, sheet_name='Descriptive Statistics', index=False)

    # Sheet 2: Normality Tests
    normality_df.to_excel(writer, sheet_name='Normality Tests', index=False)

    # Sheet 3: Pearson Correlation Matrix
    pearson_corr.to_excel(writer, sheet_name='Pearson Correlation')

    # Sheet 4: Pearson P-values
    pearson_pvalues.to_excel(writer, sheet_name='Pearson P-values')

    # Sheet 5: Spearman Correlation Matrix
    spearman_corr.to_excel(writer, sheet_name='Spearman Correlation')

    # Sheet 6: Spearman P-values
    spearman_pvalues.to_excel(writer, sheet_name='Spearman P-values')

    # Sheet 7: Detailed Correlation Results
    correlation_df.to_excel(writer, sheet_name='Correlation Details', index=False)

    # Sheet 8: Theme Scores (raw data)
    theme_scores.to_excel(writer, sheet_name='Theme Scores', index=True)

print(f"✓ All results saved to: {output_file}")
print("\n")

print("="*80)
print("ANALYSIS COMPLETE!")
print("="*80)
print("\n")
print("Files generated:")
print("  1. Normality_Correlation_Analysis.xlsx (all numerical results)")
print("  2. Normality_Assessment.png (histograms and Q-Q plots)")
print("  3. Correlation_Heatmaps.png (Pearson and Spearman heatmaps)")
print("  4. Scatter_Plot_Matrix.png (pairwise scatter plots)")
print("\n")
print("="*80)