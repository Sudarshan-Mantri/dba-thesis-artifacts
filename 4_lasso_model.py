# -*- coding: utf-8 -*-
"""4. LASSO Model"""

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
data_numeric = df.copy()

theme_definitions = {
    'Theme 1: Technical Feasibility &amp;amp; Performance': list(range(1, 15)),
    'Theme 2: Individual Acceptance (Motivators &amp;amp; Barriers)': list(range(15, 34)),
    'Theme 3: Organizational Decision-Making Factors': list(range(34, 59)),
    'Theme 4: Business Models &amp;amp; Market Strategies': list(range(59, 78))
}

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')


# LASSO Regression
lasso_results_all_themes = {}
for theme_name, question_numbers in theme_definitions.items():
    theme_cols = [str(q) for q in question_numbers]
    X = data_numeric[theme_cols].values
    y = X.mean(axis=1)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    lasso = LassoCV(cv=5, random_state=42, max_iter=10000, alphas=np.logspace(-4, 1, 100))
    lasso.fit(X_scaled, y)
    coef = lasso.coef_
    results_df = pd.DataFrame({
        'Question': [f'Q{q}' for q in question_numbers],
        'Coefficient': coef,
        'Abs_Coefficient': np.abs(coef),
        'Item_Mean': X.mean(axis=0),
        'Item_StdDev': X.std(axis=0)
    })
    results_df = results_df.sort_values('Abs_Coefficient', ascending=False)
    lasso_results_all_themes[theme_name] = {'results_df': results_df, 'r2_score': lasso.score(X_scaled, y)}

# Create visualizations
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']
theme_names_short = ['Theme 1:\nTechnical', 'Theme 2:\nAcceptance', 'Theme 3:\nOrganizational', 'Theme 4:\nBusiness Models']

# VIZ 1: Top 5 Items Per Theme
fig = plt.figure(figsize=(16, 10))
for idx, (theme_name, theme_results) in enumerate(lasso_results_all_themes.items(), 1):
    ax = plt.subplot(2, 2, idx)
    results_df = theme_results['results_df'].head(5).sort_values('Abs_Coefficient', ascending=True)
    bars = ax.barh(results_df['Question'], results_df['Abs_Coefficient'], color=colors[idx-1], alpha=0.8)
    ax.set_xlabel('Importance Score', fontsize=10, fontweight='bold')
    ax.set_title(f'{theme_names_short[idx-1]}\nTop 5 Items', fontsize=11, fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    for bar, val in zip(bars, results_df['Abs_Coefficient']):
        ax.text(val + 0.001, bar.get_y() + bar.get_height()/2, f'{val:.4f}',
                va='center', fontsize=8, fontweight='bold')

plt.tight_layout()
plt.savefig('LASSO_Top_5_Items_Per_Theme.png', dpi=300, bbox_inches='tight')
print("✓ Visualization 1: Top 5 Items Per Theme")

# VIZ 2: Theme Comparison
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

metrics = {'Top Item Importance': [], 'Average Importance': [], 'Theme': []}
for idx, (theme_name, theme_results) in enumerate(lasso_results_all_themes.items()):
    results_df = theme_results['results_df']
    metrics['Top Item Importance'].append(results_df.iloc[0]['Abs_Coefficient'])
    metrics['Average Importance'].append(results_df['Abs_Coefficient'].mean())
    metrics['Theme'].append(theme_names_short[idx])

# Plot 1: Top Item Importance
ax = axes[0]
bars = ax.bar(range(len(metrics['Theme'])), metrics['Top Item Importance'], color=colors, alpha=0.8)
ax.set_ylabel('Importance Score', fontsize=10, fontweight='bold')
ax.set_title('Most Important Item Per Theme', fontsize=11, fontweight='bold')
ax.set_xticks(range(len(metrics['Theme'])))
ax.set_xticklabels([t.replace('\n', ' ') for t in metrics['Theme']], fontsize=9)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, metrics['Top Item Importance']):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{val:.4f}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

# Plot 2: Average Importance
ax = axes[1]
bars = ax.bar(range(len(metrics['Theme'])), metrics['Average Importance'], color=colors, alpha=0.8)
ax.set_ylabel('Importance Score', fontsize=10, fontweight='bold')
ax.set_title('Average Item Importance Per Theme', fontsize=11, fontweight='bold')
ax.set_xticks(range(len(metrics['Theme'])))
ax.set_xticklabels([t.replace('\n', ' ') for t in metrics['Theme']], fontsize=9)
ax.grid(axis='y', alpha=0.3)
for bar, val in zip(bars, metrics['Average Importance']):
    ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(), f'{val:.4f}',
            ha='center', va='bottom', fontweight='bold', fontsize=9)

# Plot 3: Importance Ranking
ax = axes[2]
theme_strength = [(metrics['Theme'][i].replace('\n', ' '), metrics['Top Item Importance'][i])
                  for i in range(len(metrics['Theme']))]
theme_strength_sorted = sorted(theme_strength, key=lambda x: x[1], reverse=True)
themes_sorted = [t[0] for t in theme_strength_sorted]
strength_sorted = [t[1] for t in theme_strength_sorted]

y_pos = np.arange(len(themes_sorted))
bars = ax.barh(y_pos, strength_sorted, color=colors, alpha=0.8)
ax.set_yticks(y_pos)
ax.set_yticklabels(themes_sorted, fontsize=10)
ax.set_xlabel('Top Item Importance', fontsize=10, fontweight='bold')
ax.set_title('Theme Importance Ranking', fontsize=11, fontweight='bold')
ax.grid(axis='x', alpha=0.3)
ax.invert_yaxis()
for i, (bar, val) in enumerate(zip(bars, strength_sorted)):
    ax.text(val + 0.001, i, f'#{i+1}', va='center', fontsize=10, fontweight='bold')

# Plot 4: Summary Statistics
ax = axes[3]
ax.axis('off')
summary_text = "LASSO ANALYSIS SUMMARY\n" + "="*50 + "\n\n"
for idx, (theme_name, theme_results) in enumerate(lasso_results_all_themes.items()):
    results_df = theme_results['results_df']
    top_item = results_df.iloc[0]['Question']
    top_importance = results_df.iloc[0]['Abs_Coefficient']
    summary_text += f"{theme_names_short[idx].replace(chr(10), ' ')}\n"
    summary_text += f"  Top Item: {top_item} ({top_importance:.4f})\n"
    summary_text += f"  Avg: {results_df['Abs_Coefficient'].mean():.4f}\n\n"

ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', fontfamily='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()
plt.savefig('LASSO_Theme_Comparison.png', dpi=300, bbox_inches='tight')
print("✓ Visualization 2: Theme Comparison")

print("\nBoth visualizations saved successfully!")

# Print LASSO results for all themes
print("\n===== LASSO Results by Theme =====")
for theme_name, theme_data in lasso_results_all_themes.items():
    print(f"\nTheme: {theme_name}")
    print(theme_data['results_df'][['Question', 'Coefficient']].to_string(index=False))

print("\n===== R2 Scores by Theme =====")
for theme_name, theme_data in lasso_results_all_themes.items():
    print(f"Theme: {theme_name}\nR2 Score: {theme_data['r2_score']:.7f}")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for idx, (theme_name, theme_results) in enumerate(lasso_results_all_themes.items()):
    ax = axes[idx]
    # Sort by 'Coefficient' in descending order as requested by the user
    results_df = theme_results['results_df'].sort_values('Coefficient', ascending=False)

    sns.lineplot(x='Question', y='Coefficient', data=results_df, marker='o', ax=ax, color=colors[idx])
    ax.set_title(f'Coefficient Trend for {theme_names_short[idx]}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Question', fontsize=10)
    ax.set_ylabel('LASSO Coefficient', fontsize=10)
    ax.tick_params(axis='x', rotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Annotate points with coefficient values
    for i, point in results_df.iterrows():
        ax.text(x=point['Question'], y=point['Coefficient'], s=f'{point["Coefficient"]:.2f}',
                fontsize=8, ha='left', va='bottom', rotation=30)

plt.tight_layout()
plt.savefig('LASSO_Coefficient_Trend_Charts.png', dpi=300, bbox_inches='tight')
print("✓ Visualization 3: Coefficient Trend Charts Saved")



