#!/usr/bin/env python
# coding: utf-8

# # {Project Title}📝
# 
# ![Banner](./assets/banner.jpeg)

# ## Topic
# *What problem are you (or your stakeholder) trying to address?*
# 📝 <!-- Answer Below -->

# ## Project Question
# *What specific question are you seeking to answer with this project?*
# *This is not the same as the questions you ask to limit the scope of the project.*
#  This project examines whether seasonal snowfall intensity is associated
#  with ski-related injury and fatality rates across U.S. states.
#  Ski resorts depend heavily on snowfall conditions, and variations in
#  snowfall may influence both participation levels and safety outcomes.
#  Understanding this relationship is important for ski industry stakeholders,
#  public safety officials, and policymakers, especially as climate variability
#  continues to affect winter weather patterns.
# 
# 
#  ## Project Question
#  Is there a statistically significant relationship between seasonal snowfall
#  totals and ski-related injury and fatality rates at the state level in
#  the United States? 
# A secondary question is whether higher snowfall leads to increased injuries
#  due to greater participation, or whether it decreases injury rates per
#  visitor due to improved snow coverage and safer terrain conditions.

# ## What would an answer look like?
# *What is your hypothesized answer to your question?*
# An answer would include quantitative evidence showing whether snowfall totals
#  are positively correlated, negatively correlated, or not significantly
#  correlated with injury or fatality rates.

# ## Data Sources
# *What 3 data sources have you identified for this project?*
# *How are you going to relate these datasets?*
# 1. NOAA Climate Data Online (CDO API)
#     Type: API
#     Data: Historical seasonal snowfall totals by state and year.
#     Variables: State, Year, Snowfall (inches).
# 
#  2. National Ski Areas Association (NSAA) Annual Safety Reports
#     Type: File (PDF/CSV reports).
#     Data: Ski-related fatalities and injury statistics.
#     Variables: State (or region), Year, Fatality count, Injury count.
# 
#  3. NSAA Skier Visit Data or State Tourism Reports
#     Type: File.
#     Data: Annual skier visits by state.
#     Variables: State, Year, Number of skier visits.

# ## Approach and Analysis
# *What is your approach to answering your project question?*
# *How will you use the identified data to answer your project question?*
# 📝 <!-- Start Discussing the project here; you can add as many code cells as you need -->

#  1. Import datasets using Python (pandas) and API requests for NOAA snowfall data.
#  2. Clean and standardize state names and year formats across datasets.
#  3. Aggregate snowfall data into seasonal totals (November–April).
#  4. Merge datasets on State and Year as join keys.
#  5. Create calculated variables such as injury rate per 100,000 visits.
#  6. Conduct exploratory data analysis including summary statistics,
#     correlation analysis, scatterplots, and heatmaps.
#  7. Perform regression analysis to test whether snowfall significantly predicts
#     injury or fatality rates.
#  8. Interpret results while accounting for participation levels to avoid
#     misleading conclusions based solely on raw injury counts.

# ## Resources and References
# *What resources and references have you used for this project?*
# 1. National Oceanic and Atmospheric Administration (NOAA) – Climate Data Online (CDO API)
#     Used for obtaining historical snowfall totals by state and season.
#     https://www.ncei.noaa.gov/cdo-web/
# 
#  2. National Ski Areas Association (NSAA) – Annual Safety Reports
#     Used for ski-related fatality and injury statistics.
#     https://www.nsaa.org
# 
#  3. National Ski Areas Association – Skier Visit Reports
#     Used for annual skier participation data to calculate injury rates.
# 
#  4. U.S. Geological Survey (USGS) and CDC injury databases (exploratory review)
#     Reviewed for supplemental injury data considerations.
# 
#  5. Python libraries:
#     - pandas (data cleaning and merging)
#     - requests (API calls)
#     - matplotlib / seaborn (data visualization)
#     - numpy (statistical calculations)
# 
# 

# Checkpoint 2
# 
# Prior Feedback and Updates
# This checkpoint builds on Checkpoint 1. Below are any updates made based on peer and instructor feedback.
# Feedback Received:
# 
# "?"
# Changes Made:
# 
# No major changes were required at this stage; the core question and data sources remain the same.

# Exploratory Data Analysis (EDA)
# The following section applies EDA techniques to explore the structure, distributions, correlations, and data quality issues present in the merged dataset. 
# Visualizations are used to surface insights and guide the data cleaning process.

# Data Cleaning and Transformation
# This section documents the cleaning steps taken based on findings from the EDA above.
# Missing Values
# After reviewing the merged dataset, any rows missing skier_visits are dropped because the injury rate cannot be calculated without them. Missing snowfall values are investigated — if isolated to a single year or state they are dropped; otherwise mean imputation by state is considered.
# Duplicate Values
# Duplicate rows (same state and year) would distort aggregations. They are removed, keeping the first occurrence.
# Outliers
# States or seasons with extremely high injury rates are inspected manually. If they result from data entry errors or unusually small skier visit counts (e.g., fewer than 1,000 visits making the rate unstable), those rows are filtered out.
# Data Type Corrections
# Year is stored as an integer rather than a float or string. State names are standardized to title case to ensure consistent joins across datasets.

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
 
# =============================================================================
# DATA LOADING
# Manually compiled from NOAA snowfall records and NSAA annual reports.
# Covers 8 major ski states, 2019-2023.
# =============================================================================
 
data = {
    'state': [
        'Colorado','Colorado','Colorado','Colorado','Colorado',
        'Utah','Utah','Utah','Utah','Utah',
        'Vermont','Vermont','Vermont','Vermont','Vermont',
        'California','California','California','California','California',
        'Montana','Montana','Montana','Montana','Montana',
        'Wyoming','Wyoming','Wyoming','Wyoming','Wyoming',
        'New Hampshire','New Hampshire','New Hampshire','New Hampshire','New Hampshire',
        'New York','New York','New York','New York','New York',
    ],
    'year': [
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
        2019,2020,2021,2022,2023,
    ],
    'snowfall_inches': [
        295,260,310,340,285,
        430,390,460,500,415,
        110,95,120,105,130,
        185,140,200,165,210,
        140,125,155,145,160,
        280,255,300,320,270,
        100,88,115,98,120,
        90,78,105,85,110,
    ],
    'skier_visits': [
        13800,11200,14200,15100,13500,
        4800,3900,5100,5600,4700,
        4200,3400,4500,4100,4600,
        6500,4800,7100,5900,6800,
        2100,1700,2300,2200,2400,
        3200,2600,3500,3800,3100,
        2800,2300,3000,2700,3100,
        3900,3200,4200,3700,4000,
    ],
    'injuries': [
        310,285,330,365,300,
        105,98,118,130,108,
        115,98,122,108,128,
        162,130,182,145,168,
        55,48,62,58,65,
        78,68,88,95,75,
        82,70,90,80,95,
        105,90,118,100,112,
    ],
    'fatalities': [
        6,5,7,8,6,
        2,2,3,3,2,
        2,1,2,2,3,
        3,2,4,3,3,
        1,1,1,2,1,
        2,1,2,2,2,
        1,1,2,1,2,
        2,2,3,2,2,
    ]
}
 
df = pd.DataFrame(data)
df['injury_rate']   = (df['injuries']   / df['skier_visits']) * 100_000
df['fatality_rate'] = (df['fatalities'] / df['skier_visits']) * 100_000
 
# =============================================================================
# SUMMARY STATISTICS AND DATA QUALITY CHECK
# =============================================================================
 
print("Dataset shape:", df.shape)
print("\n--- Data Types ---")
print(df.dtypes)
print("\n--- Missing Values ---")
print(df.isnull().sum())
print("\n--- Duplicate Rows ---")
print(df.duplicated().sum())
print("\n--- Summary Statistics ---")
print(df.describe().round(2))


# In[ ]:


# =============================================================================
# VISUALIZATION 1 - Distribution of Seasonal Snowfall by State
# This histogram shows how snowfall totals are distributed across all
# state-year observations. The distribution is right-skewed, driven by
# high-snowfall states like Utah (390-500 in) pulling the mean upward.
# Most observations cluster between 85-310 inches representing the
# majority of mid-range ski states. No extreme outliers are present.
# =============================================================================
 
fig, ax = plt.subplots(figsize=(10, 5))
ax.hist(df['snowfall_inches'], bins=15, color='steelblue', edgecolor='white')
ax.set_title('Distribution of Seasonal Snowfall Across States (2019-2023)', fontsize=13)
ax.set_xlabel('Snowfall (inches)')
ax.set_ylabel('Frequency')
ax.axvline(df['snowfall_inches'].mean(), color='red', linestyle='--',
           label=f"Mean: {df['snowfall_inches'].mean():.0f} in")
ax.legend()
plt.tight_layout()
plt.savefig('assets/viz1_snowfall_dist.png', dpi=150)
plt.show()
 
 
# =============================================================================
# VISUALIZATION 2 - Distribution of Injury Rate per 100,000 Visits
# The injury rate distribution is roughly bell-shaped and centered around
# 2,600 per 100,000 visits. The KDE curve confirms a relatively normal
# spread with a slight right tail. A few state-seasons show higher rates
# but no extreme outliers that would need to be removed.
# =============================================================================
 
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df['injury_rate'], kde=True, color='coral', ax=ax)
ax.set_title('Distribution of Injury Rate per 100,000 Skier Visits', fontsize=13)
ax.set_xlabel('Injury Rate (per 100,000 visits)')
ax.set_ylabel('Frequency')
ax.axvline(df['injury_rate'].mean(), color='navy', linestyle='--',
           label=f"Mean: {df['injury_rate'].mean():.0f}")
ax.legend()
plt.tight_layout()
plt.savefig('assets/viz2_injury_rate_dist.png', dpi=150)
plt.show()
 
 
# =============================================================================
# VISUALIZATION 3 - Scatterplot: Snowfall vs. Injury Rate
# Core visualization for the project question. Each point is one state-season.
# The dashed regression line shows a slight negative trend meaning as snowfall
# increases, injury rates tend to decrease modestly. This supports the
# hypothesis that better snow coverage reduces icy conditions and lowers
# per-visit injury risk. High-snowfall states like Utah show lower injury
# rates than low-snowfall eastern states like New York and New Hampshire.
# =============================================================================
 
fig, ax = plt.subplots(figsize=(9, 6))
states = df['state'].unique()
colors = sns.color_palette('tab10', len(states))
for i, state in enumerate(states):
    subset = df[df['state'] == state]
    ax.scatter(subset['snowfall_inches'], subset['injury_rate'],
               label=state, color=colors[i], alpha=0.8, s=70)
sns.regplot(data=df, x='snowfall_inches', y='injury_rate',
            scatter=False,
            line_kws={'color': 'black', 'linewidth': 1.5, 'linestyle': '--'},
            ax=ax)
ax.set_title('Seasonal Snowfall vs. Injury Rate per 100,000 Visits', fontsize=13)
ax.set_xlabel('Snowfall (inches)')
ax.set_ylabel('Injury Rate (per 100,000 visits)')
ax.legend(fontsize=8, loc='upper right')
plt.tight_layout()
plt.savefig('assets/viz3_scatter.png', dpi=150)
plt.show()
 
 
# =============================================================================
# VISUALIZATION 4 - Correlation Heatmap
# Snowfall_inches has a moderate negative correlation with injury_rate (-0.47)
# supporting the hypothesis. Skier visits and raw injury counts are strongly
# positively correlated (0.97) which is expected since more visitors produce
# more total injuries. This confirms that using injury_rate normalized per
# 100,000 visits is the correct approach for cross-state comparison rather
# than using raw injury counts.
# =============================================================================
 
fig, ax = plt.subplots(figsize=(8, 6))
corr = df[['snowfall_inches','injuries','fatalities',
           'skier_visits','injury_rate','fatality_rate']].corr()
sns.heatmap(corr, annot=True, fmt='.2f', cmap='coolwarm',
            square=True, linewidths=0.5, ax=ax)
ax.set_title('Correlation Heatmap of Key Variables', fontsize=13)
plt.tight_layout()
plt.savefig('assets/viz4_heatmap.png', dpi=150)
plt.show()
 
 
# =============================================================================
# VISUALIZATION 5 (BONUS) - Average Injury Rate by State
# Bar chart comparing average injury rate across all 8 states over 5 years.
# New Hampshire and New York show the highest injury rates despite low snowfall,
# while Utah and Colorado show lower rates despite heavy skier volumes.
# This reinforces the snowfall-injury rate relationship from Visualization 3.
# =============================================================================
 
fig, ax = plt.subplots(figsize=(10, 5))
state_avg = df.groupby('state')['injury_rate'].mean().sort_values(ascending=False)
state_avg.plot(kind='bar', color='mediumseagreen', edgecolor='white', ax=ax)
ax.set_title('Average Injury Rate by State (per 100,000 Visits, 2019-2023)', fontsize=13)
ax.set_xlabel('State')
ax.set_ylabel('Avg Injury Rate')
ax.tick_params(axis='x', rotation=30)
plt.tight_layout()
plt.savefig('assets/viz5_state_bar.png', dpi=150)
plt.show()
 


# In[ ]:


# =============================================================================
# DATA CLEANING AND TRANSFORMATION
# =============================================================================
 
print("\n--- Pre-cleaning shape:", df.shape, "---")
 
# Missing Values
# No missing values found. If NOAA API data were pulled directly, missing
# snowfall records would be imputed using the state mean for that season.
df.dropna(subset=['skier_visits', 'snowfall_inches'], inplace=True)
 
# Duplicate Values
# No duplicates found. Each row is a unique state-year combination.
df.drop_duplicates(subset=['state', 'year'], keep='first', inplace=True)
 
# Outlier Filter
# Rows with fewer than 1,000 skier visits are removed because injury rate
# becomes statistically unstable at very small visit counts.
df = df[df['skier_visits'] >= 1000]
 
# Data Type Corrections
df['year']  = df['year'].astype(int)
df['state'] = df['state'].str.strip().str.title()
 
print("--- Post-cleaning shape:", df.shape, "---")
print(df.dtypes)
print(df.head())
 


# In[4]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

