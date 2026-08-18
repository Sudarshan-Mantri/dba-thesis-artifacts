# -*- coding: utf-8 -*-
"""2. Demographic Analysis"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

## Import file
from google.colab import files
uploaded = files.upload()

for fn in uploaded.keys():
  print('User uploaded file "{name}" with length {length} bytes'.format(
      name=fn, length=len(uploaded[fn])))

  df = pd.read_excel(fn)

display(df.head())

# Clean all string columns by removing leading/trailing spaces
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].str.strip()

print("✅ Data loaded and cleaned!")
print(f"Total respondents: {len(df)}")

# Clean the data - COMPREHENSIVE CLEANING
df['Role'] = df['Role'].str.replace('\xa0', ' ').str.replace('\u2013', '–').str.strip()
df['Company'] = df['Company'].str.replace('\xa0', ' ').str.strip()
df['Domain'] = df['Domain'].str.replace('\xa0', ' ').str.strip()
df['Exposure'] = df['Exposure'].str.strip()
df['Training'] = df['Training'].str.strip()

# ============================================================================
# TABLE 4.1: COMPANY TYPE DISTRIBUTION
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.1: COMPANY TYPE DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

company_dist = df['Company'].value_counts().reset_index()
company_dist.columns = ['Company Type', 'Frequency']
company_dist['Percentage'] = round((company_dist['Frequency'] / len(df)) * 100, 2)
company_dist = company_dist.sort_values('Frequency', ascending=False)
company_dist.index = range(1, len(company_dist) + 1)

print(company_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({company_dist['Percentage'].sum():.2f}%)")

# ============================================================================
# TABLE 4.2: PROFESSIONAL DOMAIN DISTRIBUTION (GROUPED)
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.2: PROFESSIONAL DOMAIN DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

# Create domain grouping
domain_mapping = {
    'Software Development / AI & ML Engineering': 'Technology Development & AI',
    'Industrial Automation / System Integration & IoT': 'Automation & Integration',
    'Manufacturing Process / Production Lines': 'Manufacturing Operations',
    'Procurement / Finance / Sales': 'Business & Procurement',
    'Research, Design and Development': 'R&D and Innovation',
    'Sensor Technology (Hardware or Software Sensors)': 'R&D and Innovation',
    'Innovation Mgt.': 'R&D and Innovation',
    'PLM': 'R&D and Innovation',
    'Academics / Research': 'R&D and Innovation'
}

df['Domain_Grouped'] = df['Domain'].map(domain_mapping)

# Check for unmapped values
unmapped = df[df['Domain_Grouped'].isna()]['Domain'].unique()
if len(unmapped) > 0:
    print("\nWARNING: Unmapped domain values found:")
    for val in unmapped:
        print(f"   - '{val}'")
    print()

domain_dist = df['Domain_Grouped'].value_counts().reset_index()
domain_dist.columns = ['Professional Domain', 'Frequency']
domain_dist['Percentage'] = round((domain_dist['Frequency'] / len(df)) * 100, 2)
domain_dist = domain_dist.sort_values('Frequency', ascending=False)
domain_dist.index = range(1, len(domain_dist) + 1)

print(domain_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({domain_dist['Percentage'].sum():.2f}%)")

print("\n" + "-" * 80)
print("Note: Professional domains were grouped from original categories")
print("-" * 80)

# ============================================================================
# TABLE 4.3: JOB ROLE/FUNCTION DISTRIBUTION (GROUPED)
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.3: JOB ROLE/FUNCTION DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

# Create role grouping
role_mapping = {
    'Technology Development – I design, develop, or implement technology solutions, products or services as part of a focused technical team.': 'Technology Development',
    'Supervision / Middle Management – I coordinate cross-functional teams and lead project-level, product level, solution level decisions for technology initiatives.': 'Supervision & Management',
    'Technical/Financial Evaluation – I evaluate technical/financial options and provide recommendations to support technology selection.': 'Technical/Financial Evaluation',
    'Strategic Leadership – I lead and manage high-level strategy and decision-making regarding technology adoption.': 'Strategic Leadership',
    'Operate / Maintain / Use – I operate or maintain technology solutions directly in day-to-day production or in machines.': 'Operations & Maintenance',
    'Sales Operation': 'Sales & Business Development',
    'Sales': 'Sales & Business Development'
}

df['Role_Grouped'] = df['Role'].map(role_mapping)

role_dist = df['Role_Grouped'].value_counts().reset_index()
role_dist.columns = ['Job Role/Function', 'Frequency']
role_dist['Percentage'] = round((role_dist['Frequency'] / len(df)) * 100, 2)
role_dist = role_dist.sort_values('Frequency', ascending=False)
role_dist.index = range(1, len(role_dist) + 1)

print(role_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({role_dist['Percentage'].sum():.2f}%)")

# ============================================================================
# TABLE 4.4: EXPERIENCE LEVEL DISTRIBUTION
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.4: PROFESSIONAL EXPERIENCE DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

# Define experience order
experience_order = [
    'Less than 2 Years',
    '2 to 5 Years',
    '6 to 10 Years',
    '11 to 15 Years',
    '16 to 20 Years',
    'More than 20 Years'
]

exp_dist = df['Experience'].value_counts().reset_index()
exp_dist.columns = ['Experience Level', 'Frequency']
exp_dist['Percentage'] = round((exp_dist['Frequency'] / len(df)) * 100, 2)

# Sort by defined order
exp_dist['Experience Level'] = pd.Categorical(exp_dist['Experience Level'],
                                               categories=experience_order,
                                               ordered=True)
exp_dist = exp_dist.sort_values('Experience Level')
exp_dist.index = range(1, len(exp_dist) + 1)

print(exp_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({exp_dist['Percentage'].sum():.2f}%)")

# Calculate statistics
print("\n" + "-" * 80)
print("Experience Distribution Summary:")
exp_high = exp_dist[exp_dist['Experience Level'].isin(['11 to 15 Years', '16 to 20 Years', 'More than 20 Years'])]['Frequency'].sum()
exp_high_pct = round((exp_high / len(df)) * 100, 2)
print(f"  • Highly experienced (>10 years): {exp_high} ({exp_high_pct}%)")

exp_mid = exp_dist[exp_dist['Experience Level'].isin(['6 to 10 Years'])]['Frequency'].sum()
exp_mid_pct = round((exp_mid / len(df)) * 100, 2)
print(f"  • Mid-level experience (6-10 years): {exp_mid} ({exp_mid_pct}%)")

exp_low = exp_dist[exp_dist['Experience Level'].isin(['2 to 5 Years', 'Less than 2 Years'])]['Frequency'].sum()
exp_low_pct = round((exp_low / len(df)) * 100, 2)
print(f"  • Early career (<6 years): {exp_low} ({exp_low_pct}%)")
print("-" * 80)

# ============================================================================
# TABLE 4.5: EXPOSURE LEVEL DISTRIBUTION
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.5: TECHNOLOGY EXPOSURE DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

# Define exposure order (High to None)
exposure_order = [
    'High (Expertise & Leadership in AI implementation topics)',
    'Moderate (Regular use or involvement in AI-related topics)',
    'Low (Occasional use of AI in work / projects)',
    'None (No direct interaction with AI technologies)'
]

exposure_dist = df['Exposure'].value_counts().reset_index()
exposure_dist.columns = ['Exposure Level', 'Frequency']
exposure_dist['Percentage'] = round((exposure_dist['Frequency'] / len(df)) * 100, 2)

# Sort by defined order
exposure_dist['Exposure Level'] = pd.Categorical(exposure_dist['Exposure Level'],
                                                  categories=exposure_order,
                                                  ordered=True)
exposure_dist = exposure_dist.sort_values('Exposure Level')
exposure_dist.index = range(1, len(exposure_dist) + 1)

print(exposure_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({exposure_dist['Percentage'].sum():.2f}%)")

# Calculate statistics
print("\n" + "-" * 80)
print("Exposure Distribution Summary:")
exp_high_mod = exposure_dist[exposure_dist['Exposure Level'].isin([
    'High (Expertise & Leadership in AI implementation topics)',
    'Moderate (Regular use or involvement in AI-related topics)'
])]['Frequency'].sum()
exp_high_mod_pct = round((exp_high_mod / len(df)) * 100, 2)
print(f"  • High to Moderate exposure: {exp_high_mod} ({exp_high_mod_pct}%)")
print("-" * 80)

# ============================================================================
# TABLE 4.6: TRAINING BACKGROUND DISTRIBUTION
# ============================================================================
print("\n" + "=" * 80)
print("TABLE 4.6: TRAINING BACKGROUND DISTRIBUTION OF RESPONDENTS")
print("=" * 80)

# Define training order
training_order = [
    'Advanced training (e.g. Certifications, Academic Degrees, Specialized courses)',
    'Basic Training (e.g. Introductory courses or workshops)',
    'On-the-Job training (e.g. Practical work experience, Part of Projects, Professional Hands-on)',
    'No Training / Self Reading'
]

training_dist = df['Training'].value_counts().reset_index()
training_dist.columns = ['Training Background', 'Frequency']
training_dist['Percentage'] = round((training_dist['Frequency'] / len(df)) * 100, 2)

# Sort by defined order
training_dist['Training Background'] = pd.Categorical(training_dist['Training Background'],
                                                       categories=training_order,
                                                       ordered=True)
training_dist = training_dist.sort_values('Training Background')
training_dist.index = range(1, len(training_dist) + 1)

print(training_dist.to_string())
print(f"\nTotal: {len(df)} respondents ({training_dist['Percentage'].sum():.2f}%)")

# Calculate statistics
print("\n" + "-" * 80)
print("Training Distribution Summary:")
formal_training = training_dist[training_dist['Training Background'].isin([
    'Advanced training (e.g. Certifications, Academic Degrees, Specialized courses)',
    'Basic Training (e.g. Introductory courses or workshops)'
])]['Frequency'].sum()
formal_pct = round((formal_training / len(df)) * 100, 2)
print(f"  • Formal training (Advanced + Basic): {formal_training} ({formal_pct}%)")

practical = training_dist[training_dist['Training Background'] ==
    'On-the-Job training (e.g. Practical work experience, Part of Projects, Professional Hands-on)']['Frequency'].sum()
practical_pct = round((practical / len(df)) * 100, 2)
print(f"  • Practical/On-the-Job training: {practical} ({practical_pct}%)")
print("-" * 80)

# ============================================================================
# SUMMARY STATISTICS
# ============================================================================
print("\n" + "=" * 80)
print("DEMOGRAPHIC PROFILE SUMMARY")
print("=" * 80)

print(f"\nTotal Valid Responses: {len(df)}")

print("\nCompany Profile:")
top_company = company_dist.iloc[0]
print(f"   • Dominant sector: {top_company['Company Type']} ({top_company['Percentage']}%)")

print("\nProfessional Profile:")
top_domain = domain_dist.iloc[0]
print(f"   • Primary domain: {top_domain['Professional Domain']} ({top_domain['Percentage']}%)")
top_role = role_dist.iloc[0]
print(f"   • Primary role: {top_role['Job Role/Function']} ({top_role['Percentage']}%)")

print("\nExperience Profile:")
print(f"   • Highly experienced professionals (>10 years): {exp_high_pct}%")

print("\nTechnology Exposure:")
print(f"   • High to Moderate AI exposure: {exp_high_mod_pct}%")

print("\nTraining Background:")
print(f"   • Formal training received: {formal_pct}%")

print("\n" + "=" * 80)
print("ALL DEMOGRAPHIC TABLES COMPLETED")
print("=" * 80)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for professional academic visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9


# Clean the data
df['Role'] = df['Role'].str.replace('\xa0', ' ').str.replace('\u2013', '–').str.strip()
df['Company'] = df['Company'].str.replace('\xa0', ' ').str.strip()
df['Domain'] = df['Domain'].str.replace('\xa0', ' ').str.strip()
df['Exposure'] = df['Exposure'].str.strip()
df['Training'] = df['Training'].str.strip()

# Apply groupings
domain_mapping = {
    'Software Development / AI &amp; ML Engineering': 'Technology Development &amp; AI',
    'Industrial Automation / System Integration &amp; IoT': 'Automation &amp; Integration',
    'Manufacturing Process / Production Lines': 'Manufacturing Operations',
    'Procurement / Finance / Sales': 'Business &amp; Procurement',
    'Research, Design and Development': 'R&amp;D and Innovation',
    'Sensor Technology (Hardware or Software Sensors)': 'R&amp;D and Innovation',
    'Innovation Mgt.': 'R&amp;D and Innovation',
    'PLM': 'R&amp;D and Innovation',
    'Academics / Research': 'R&amp;D and Innovation'
}

role_mapping = {
    'Technology Development – I design, develop, or implement technology solutions, products or services as part of a focused technical team.': 'Technology Development',
    'Supervision / Middle Management – I coordinate cross-functional teams and lead project-level, product level, solution level decisions for technology initiatives.': 'Supervision &amp; Management',
    'Technical/Financial Evaluation – I evaluate technical/financial options and provide recommendations to support technology selection.': 'Technical/Financial Evaluation',
    'Strategic Leadership – I lead and manage high-level strategy and decision-making regarding technology adoption.': 'Strategic Leadership',
    'Operate / Maintain / Use – I operate or maintain technology solutions directly in day-to-day production or in machines.': 'Operations &amp; Maintenance',
    'Sales Operation': 'Sales &amp; Business Development',
    'Sales': 'Sales &amp; Business Development'
}

df['Domain_Grouped'] = df['Domain'].map(domain_mapping)
df['Role_Grouped'] = df['Role'].map(role_mapping)

# Create color palettes
color_palette_main = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f']
color_palette_blue = sns.color_palette("Blues_d", 8)
color_palette_green = sns.color_palette("Greens_d", 6)

# ============================================================================
# FIGURE 4.1: COMPANY TYPE DISTRIBUTION
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

company_dist = df['Company'].value_counts().sort_values(ascending=True)
colors = sns.color_palette("viridis", len(company_dist))

company_dist.plot(kind='barh', ax=ax, color=colors, edgecolor='black', linewidth=0.7)

ax.set_xlabel('Frequency', fontweight='bold')
ax.set_ylabel('Company Type', fontweight='bold')
ax.set_title('Figure 4.1: Company Type Distribution of Respondents (N=65)',
             fontweight='bold', pad=20)

# Add value labels
for i, v in enumerate(company_dist.values):
    percentage = (v / len(df)) * 100
    ax.text(v + 0.5, i, f'{v} ({percentage:.1f}%)',
            va='center', fontsize=9)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/Figure_4_1_Company_Type.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.1 saved: Company Type Distribution")
plt.close()

# ============================================================================
# FIGURE 4.2: PROFESSIONAL DOMAIN DISTRIBUTION (PIE CHART)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 8))

domain_dist = df['Domain_Grouped'].value_counts()
colors_domain = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

wedges, texts, autotexts = ax.pie(domain_dist.values,
                                    labels=domain_dist.index,
                                    autopct='%1.1f%%',
                                    startangle=90,
                                    colors=colors_domain,
                                    textprops={'fontsize': 10},
                                    wedgeprops={'edgecolor': 'white', 'linewidth': 2})

# Make percentage text bold
for autotext in autotexts:
    autotext.set_color('white')
    autotext.set_fontweight('bold')
    autotext.set_fontsize(11)

ax.set_title('Figure 4.2: Professional Domain Distribution of Respondents (N=65)',
             fontweight='bold', pad=20, fontsize=13)

plt.tight_layout()
plt.savefig('/tmp/Figure_4_2_Professional_Domain.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.2 saved: Professional Domain Distribution")
plt.close()

# ============================================================================
# FIGURE 4.3: JOB ROLE/FUNCTION DISTRIBUTION
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

role_dist = df['Role_Grouped'].value_counts().sort_values(ascending=True)
colors_role = sns.color_palette("coolwarm", len(role_dist))

role_dist.plot(kind='barh', ax=ax, color=colors_role, edgecolor='black', linewidth=0.7)

ax.set_xlabel('Frequency', fontweight='bold')
ax.set_ylabel('Job Role/Function', fontweight='bold')
ax.set_title('Figure 4.3: Job Role/Function Distribution of Respondents (N=65)',
             fontweight='bold', pad=20)

# Add value labels
for i, v in enumerate(role_dist.values):
    percentage = (v / len(df)) * 100
    ax.text(v + 0.5, i, f'{v} ({percentage:.1f}%)',
            va='center', fontsize=9)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/Figure_4_3_Job_Role.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.3 saved: Job Role/Function Distribution")
plt.close()

# ============================================================================
# FIGURE 4.4: PROFESSIONAL EXPERIENCE DISTRIBUTION
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

experience_order = [
    'Less than 2 Years',
    '2 to 5 Years',
    '6 to 10 Years',
    '11 to 15 Years',
    '16 to 20 Years',
    'More than 20 Years'
]

exp_dist = df['Experience'].value_counts()
exp_dist = exp_dist.reindex(experience_order)

colors_exp = ['#d4e6f1', '#a9cce3', '#7fb3d5', '#5499c7', '#2e86c1', '#1b4f72']

exp_dist.plot(kind='bar', ax=ax, color=colors_exp, edgecolor='black', linewidth=0.7)

ax.set_xlabel('Experience Level', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('Figure 4.4: Professional Experience Distribution of Respondents (N=65)',
             fontweight='bold', pad=20)
ax.set_xticklabels(exp_dist.index, rotation=45, ha='right')

# Add value labels
for i, v in enumerate(exp_dist.values):
    percentage = (v / len(df)) * 100
    ax.text(i, v + 0.5, f'{v}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontsize=9)

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/Figure_4_4_Experience.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.4 saved: Professional Experience Distribution")
plt.close()

# ============================================================================
# FIGURE 4.5: TECHNOLOGY EXPOSURE DISTRIBUTION
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

exposure_order = [
    'High (Expertise &amp; Leadership in AI implementation topics)',
    'Moderate (Regular use or involvement in AI-related topics)',
    'Low (Occasional use of AI in work / projects)',
    'None (No direct interaction with AI technologies)'
]

exposure_dist = df['Exposure'].value_counts()
exposure_dist = exposure_dist.reindex(exposure_order)

# Shorten labels for visualization
exposure_labels = ['High', 'Moderate', 'Low', 'None']
colors_exposure = ['#27ae60', '#f39c12', '#e74c3c', '#95a5a6']

bars = ax.bar(exposure_labels, exposure_dist.values, color=colors_exposure,
              edgecolor='black', linewidth=0.7)

ax.set_xlabel('Technology Exposure Level', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('Figure 4.5: Technology Exposure Distribution of Respondents (N=65)',
             fontweight='bold', pad=20)

# Add value labels
for i, (bar, v) in enumerate(zip(bars, exposure_dist.values)):
    percentage = (v / len(df)) * 100
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.5,
            f'{v}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/Figure_4_5_Exposure.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.5 saved: Technology Exposure Distribution")
plt.close()

# ============================================================================
# FIGURE 4.6: TRAINING BACKGROUND DISTRIBUTION
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

training_order = [
    'Advanced training (e.g. Certifications, Academic Degrees, Specialized courses)',
    'Basic Training (e.g. Introductory courses or workshops)',
    'On-the-Job training (e.g. Practical work experience, Part of Projects, Professional Hands-on)',
    'No Training / Self Reading'
]

training_dist = df['Training'].value_counts()
training_dist = training_dist.reindex(training_order)

# Shorten labels
training_labels = ['Advanced\nTraining', 'Basic\nTraining', 'On-the-Job\nTraining', 'No Training/\nSelf Reading']
colors_training = ['#8e44ad', '#3498db', '#16a085', '#e67e22']

bars = ax.bar(training_labels, training_dist.values, color=colors_training,
              edgecolor='black', linewidth=0.7)

ax.set_xlabel('Training Background', fontweight='bold')
ax.set_ylabel('Frequency', fontweight='bold')
ax.set_title('Figure 4.6: Training Background Distribution of Respondents (N=65)',
             fontweight='bold', pad=20)

# Add value labels
for i, (bar, v) in enumerate(zip(bars, training_dist.values)):
    percentage = (v / len(df)) * 100
    ax.text(bar.get_x() + bar.get_width()/2, v + 0.5,
            f'{v}\n({percentage:.1f}%)',
            ha='center', va='bottom', fontsize=10, fontweight='bold')

ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/tmp/Figure_4_6_Training.png', dpi=300, bbox_inches='tight')
print("✅ Figure 4.6 saved: Training Background Distribution")
plt.close()

print("\n" + "="*80)
print("ALL 6 FIGURES GENERATED SUCCESSFULLY!")
print("="*80)
print("\nFiles saved:")
print("  • Figure_4_1_Company_Type.png")
print("  • Figure_4_2_Professional_Domain.png")
print("  • Figure_4_3_Job_Role.png")
print("  • Figure_4_4_Experience.png")
print("  • Figure_4_5_Exposure.png")
print("  • Figure_4_6_Training.png")
print("\nAll figures are high-resolution (300 DPI) and ready for thesis insertion.")
print("="*80)

