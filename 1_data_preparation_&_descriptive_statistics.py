# -*- coding: utf-8 -*-
"""1. Data Preparation & Descriptive Statistics"""

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

# Calculate descriptive statistics
desc_stats = df_numeric[question_cols].describe().T
desc_stats['median'] = df_numeric[question_cols].median()
desc_stats['mode'] = df_numeric[question_cols].mode().iloc[0]
desc_stats['variance'] = df_numeric[question_cols].var()
desc_stats = desc_stats[['count', 'mean', 'median', 'mode', 'std', 'variance', 'min', 'max']]
desc_stats = desc_stats.round(2)

# Save
desc_stats.to_excel('Descriptive_Statistics.xlsx')
print(desc_stats.head(10))

# Define all 77 questions based on the questionnaire
questions = {
    # Theme 1: Technical feasibility and performance (Q1-Q14)
    1: "AI-based software sensors deliver performance equivalent to or superior to traditional hardware sensors",
    2: "The choice of sensing method does not matter if machine performance remains consistent",
    3: "Production machines can operate effectively when all hardware sensors replaced by AI-based software sensors",
    4: "AI-based software sensors exhibit greater reliability than hardware sensors",
    5: "Hybrid systems using both hardware and AI-based software sensors are better",
    6: "AI-based software sensors are better in shopfloor connectivity",
    7: "AI-based software sensors adapt better to evolving manufacturing processes",
    8: "Data accuracy in AI-based software sensors degrades faster than hardware sensors",
    9: "AI-based software sensors meet machine safety requirements as effectively as hardware sensors",
    10: "Global differences in AI regulations are a barrier for adoption",
    11: "AI-based software sensors are not yet safe for widespread industrial deployment",
    12: "Observability features make AI-based sensors acceptable for shopfloor use",
    13: "Regulators and Auditors show reluctance to support machinery with AI-based software sensors",
    14: "Cybersecurity vulnerabilities in AI-based software sensors pose significant risks",

    # Theme 2: Individual Acceptance - Trust (Q15-Q21)
    15: "Output of AI-based software sensors require less monitoring than hardware sensors",
    16: "Understanding the method by which AI-based sensors generate measurements is critical for trust",
    17: "Integration of AI models in software sensors plants hesitation among plant personnel",
    18: "Third-party certifications enhance confidence in implementing AI-based software sensors",
    19: "AI-based software sensors cannot be fully trusted for industry-grade operations",
    20: "Ethical concerns about AI decision-making reduce trust",
    21: "Earlier bad experience with AI reduces trust in new machines with AI based sensors",

    # Theme 2: Change Resistance (Q22-Q27)
    22: "Demonstrating clear benefits reduces resistance to adopt AI-based sensors",
    23: "Resistance is limited to users who directly interact with machines",
    24: "Plant personnel at all levels can resist even when benefits are demonstrated",
    25: "Peer champions and local advocates facilitate greater acceptance",
    26: "Access to rapid support channels boosts acceptance",
    27: "Presence of AI-powered sensors increases concerns about job displacement",

    # Theme 2: User Training (Q28-Q33)
    28: "Adequate training enhances user-acceptance of AI-based sensors",
    29: "User-friendliness is equally important as technical performance",
    30: "Training is necessary even when outsourced to technology vendors",
    31: "Lack of knowledge is the primary usage barrier",
    32: "Small continuous training programs give better results than one-time extensive training",
    33: "Training requirements are same for shopfloor teams and business leaders",

    # Theme 3: Organizational Decision Making - Leadership (Q34-Q40)
    34: "Company leadership has more visibility around AI-based sensing technologies",
    35: "Endorsement from top leadership is enough for all plant personnel to accept",
    36: "Middle and lower management have no role once top leadership approves",
    37: "Internal alignment occurs naturally when AI-based sensing is prioritized",
    38: "Conflicting departmental priorities slow down adoption",
    39: "Ambiguous organizational policies can delay sensor transition projects",
    40: "Organizational culture emphasizing innovation sees faster adoption",

    # Theme 3: ROI and Budgeting (Q41-Q46)
    41: "AI-based software sensors provide superior ROI compared to hardware sensors",
    42: "Budget uncertainties make AI-based sensor projects impractical",
    43: "Hidden costs are the main barrier to adoption initiatives",
    44: "Estimating financial impact is unnecessary because value is already established",
    45: "Investments justified as they reduce downtime and need fewer replacements",
    46: "Post-adoption monitoring is essential for evaluating success",

    # Theme 3: Pilot Testing (Q47-Q53)
    47: "Pilot testing is essential prior to full rollout",
    48: "Successful pilot testing accelerates adoption and acceptance",
    49: "Pilot testing represents unnecessary overhead",
    50: "Resource constraints in pilot testing limits accurate assessment",
    51: "Successful pilot testing should trigger full deployment rather than phased approach",
    52: "Cross-functional teams are critical for mitigating risks",
    53: "Challenges of adopting AI-based sensors are different for each sector",

    # Theme 3: Operational Risk (Q54-Q58)
    54: "Transitioning supports long-term business continuity",
    55: "AI-based sensors introduce operational failure risks unfamiliar to manufacturing",
    56: "Hardware sensors can serve as reliable backups for AI-based systems",
    57: "Diagnosing failures is challenging without specialized support mechanisms",
    58: "AI-based software sensors represent the future standard for sensing",

    # Theme 4: Business Models - Value Proposition (Q59-Q63)
    59: "AI-based software sensors enable unique features not achievable with hardware sensors",
    60: "AI-based sensing delivers significant value in Greenfield rather than Brownfield",
    61: "Large scale Manufacturing companies would be first to show interest",
    62: "Competitive pressures and market dynamics drive adoption",
    63: "Interest is driven more by industry hype than by proven results",

    # Theme 4: Vendor Partnership (Q64-Q70)
    64: "Manufacturing plants should leverage experienced vendors",
    65: "Developing in-house is preferable to purchasing from external vendors",
    66: "AI-based sensor technologies need expertise beyond day-to-day operations",
    67: "Vendors should be allowed to use proprietary black-box AI models if it adds value",
    68: "Intensive scrutiny makes vendor-user partnerships impractical",
    69: "Decision on Data sovereignty is a pre-requisite for vendor partnerships",
    70: "Supporting shopfloor hardware should also be in technology provider's scope",

    # Theme 4: Pricing &amp;amp; SaaS Models (Q71-Q77)
    71: "Favorable pricing models encourage broader adoption",
    72: "SaaS is the preferred model for acquiring AI-based sensing technology",
    73: "Usage-based variable pricing is unacceptable",
    74: "Value-based or outcome-based pricing is superior to SaaS",
    75: "SaaS pricing models act as a barrier to acceptance and adoption",
    76: "Scalability across multiple facilities influences choice of business model",
    77: "Combining SaaS variants can be convenient for manufacturing companies"
}

# Create numeric dataframe
df_numeric = df.copy()
question_cols = [str(i) for i in range(1, 78)]

# Convert to numeric
for col in question_cols:
    df_numeric[col] = df_numeric[col].map(likert_mapping)

# Calculate descriptive statistics
desc_stats = df_numeric[question_cols].describe().T
desc_stats['median'] = df_numeric[question_cols].median()
desc_stats['mode'] = df_numeric[question_cols].mode().iloc[0]
desc_stats['variance'] = df_numeric[question_cols].var()
desc_stats = desc_stats[['count', 'mean', 'median', 'mode', 'std', 'variance', 'min', 'max']]
desc_stats = desc_stats.round(3)

# Add questions
desc_stats['Question'] = desc_stats.index.astype(int).map(questions)

# Save the file to the current content directory for easier access
desc_stats.to_excel('Descriptive_Statistics_with_Questions.xlsx')

print("="*100)
print("DESCRIPTIVE STATISTICS WITH QUESTION MAPPING")
print("="*100)

# Identify key findings
print("\n🔝 TOP 5 HIGHEST AGREEMENT (Mean Score):")
print("-"*100)
top5 = desc_stats.nlargest(5, 'mean')[['mean', 'std', 'Question']]
for idx, row in top5.iterrows():
    print(f"Q{idx}: M={row['mean']:.2f}, SD={row['std']:.2f}")
    print(f"   → {row['Question']}")
    print()

print("\n🔻 TOP 5 LOWEST AGREEMENT (Mean Score):")
print("-"*100)
bottom5 = desc_stats.nsmallest(5, 'mean')[['mean', 'std', 'Question']]
for idx, row in bottom5.iterrows():
    print(f"Q{idx}: M={row['mean']:.2f}, SD={row['std']:.2f}")
    print(f"   → {row['Question']}")
    print()

print("\n🎯 STRONGEST CONSENSUS (Lowest Standard Deviation):")
print("-"*100)
consensus5 = desc_stats.nsmallest(5, 'std')[['mean', 'std', 'Question']]
for idx, row in consensus5.iterrows():
    print(f"Q{idx}: M={row['mean']:.2f}, SD={row['std']:.2f}")
    print(f"   → {row['Question']}")
    print()

print("\n🔀 MOST DIVERGENT OPINIONS (Highest Standard Deviation):")
print("-"*100)
divergent5 = desc_stats.nlargest(5, 'std')[['mean', 'std', 'Question']]
for idx, row in divergent5.iterrows():
    print(f"Q{idx}: M={row['mean']:.2f}, SD={row['std']:.2f}")
    print(f"   → {row['Question']}")
    print()

# Count mode distribution
mode_counts = desc_stats['mode'].value_counts().sort_index()
print("\n📊 MODE DISTRIBUTION:")
print("-"*100)
for mode_val, count in mode_counts.items():
    print(f"Mode {int(mode_val)}: {count} questions")

print("\n✅ Files saved:")
print("   - Descriptive_Statistics_with_Questions.xlsx")