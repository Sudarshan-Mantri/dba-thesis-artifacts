# DBA Thesis: Statistical Analysis Code

Python scripts supporting the quantitative analysis in:

**"Exploring Acceptance and Adoption Preferences for AI-Based Software Sensors as Replacements for Hardware Sensors in Active Production Lines"**

Sudarshan Mantri, DBA, ESGCI Paris, 2026

## Files

| File | Purpose |
|------|---------|
| `1_data_preparation_&_descriptive_statistics.py` | Likert mapping, descriptive statistics for 77 survey items |
| `2_demographic_analysis.py` | Demographic frequency tables and visualizations |
| `3_reliability,_normality_&_correlation.py` | Cronbach's Alpha, Shapiro-Wilk normality, Pearson and Spearman correlations |
| `4_lasso_model.py` | LASSO regression for item importance ranking per theme |
| `rc_and_descriptive_statistics.py` | Reverse coding verification; confirmed original data structure is more suitable, so all thesis analyses use non-reverse-coded data |

## Environment

All scripts run on Google Colab. Each prompts for the survey Excel file on execution.

Dependencies: pandas, numpy, scipy, scikit-learn, matplotlib, seaborn
