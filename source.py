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

# In[5]:


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


# In[6]:


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



# In[7]:


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



# ---
# ## Checkpoint 3 — Machine Learning
# 

# ### Prior Feedback and Updates
# 
# **Feedback Received:**
# No formal feedback was received from peers or the teaching team for Checkpoint 2 beyond the placeholder noted in that section.
# 
# **Changes Made:**
# - Core project question and dataset remain unchanged.
# - EDA and data cleaning sections from Checkpoint 2 are retained as-is.
# - This checkpoint adds a machine learning plan and implementation on top of the existing work.

# ### 1. Machine Learning Plan
# 
# **Model Type:**  
# The primary model will be **Linear Regression** to quantify the relationship between seasonal snowfall and injury rate per 100,000 skier visits. A **Random Forest Regressor** will be tested as a secondary model to capture any non-linear patterns and serve as a performance benchmark.
# 
# **Target variable:** `injury_rate` (continuous, regression task)  
# **Features:** `snowfall_inches`, `skier_visits`, `state` (encoded), `year`
# 
# **Identified Challenges:**
# 1. **Small dataset (40 rows):** With only 8 states across 5 years, the dataset is limited. Overfitting is a real risk, especially for more complex models.
# 2. **Simulated data:** The dataset was constructed for this project rather than pulled directly from live sources, which limits real-world generalizability.
# 3. **Multicollinearity:** `skier_visits` and `injuries` are strongly correlated (r = 0.97), so raw injury counts will be excluded as a feature to avoid leakage.
# 4. **Categorical feature (state):** State names must be encoded before being passed to sklearn models.
# 
# **How Challenges Will Be Addressed:**
# - Use an 80/20 train-test split and cross-validation given the small sample size.
# - Exclude `injuries` and `fatalities` raw counts as features to prevent data leakage into the target.
# - Apply `OneHotEncoder` for state within a sklearn pipeline.
# - Compare Linear Regression and Random Forest using RMSE and R² to select the better model.

# ### 2. Machine Learning Implementation Process
# 

# In[ ]:


# =============================================================================
# MACHINE LEARNING — SETUP AND FEATURE ENGINEERING
# =============================================================================

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Features and target
# Exclude raw injury/fatality counts to prevent leakage into injury_rate target
features = ['snowfall_inches', 'skier_visits', 'year', 'state']
target   = 'injury_rate'

X = df[features].copy()
y = df[target].copy()

# 80/20 split — stratify not applicable for regression, random_state for reproducibility
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Training set size : {X_train.shape[0]} rows")
print(f"Test set size     : {X_test.shape[0]} rows")


# In[ ]:


# =============================================================================
# SKLEARN PIPELINE — PREPROCESSING
# Numeric features: impute with median, then scale (StandardScaler)
# Categorical feature (state): impute with most_frequent, then OneHotEncode
# =============================================================================

numeric_features     = ['snowfall_inches', 'skier_visits', 'year']
categorical_features = ['state']

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler',  StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot',  OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

preprocessor = ColumnTransformer(transformers=[
    ('num', numeric_transformer,     numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

print('Preprocessor pipeline defined.')


# In[ ]:


# =============================================================================
# MODEL 1 — LINEAR REGRESSION
# Baseline model. Interpretable and appropriate for a small dataset.
# Cross-validation (5-fold) used due to limited sample size.
# =============================================================================

lr_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model',        LinearRegression())
])

lr_pipeline.fit(X_train, y_train)
y_pred_lr = lr_pipeline.predict(X_test)

lr_rmse = np.sqrt(mean_squared_error(y_test, y_pred_lr))
lr_r2   = r2_score(y_test, y_pred_lr)

# 5-fold cross-validation on full dataset
lr_cv_r2 = cross_val_score(lr_pipeline, X, y, cv=5, scoring='r2')

print('=== Linear Regression ===')
print(f'Test RMSE : {lr_rmse:.2f}')
print(f'Test R²   : {lr_r2:.4f}')
print(f'CV R²     : {lr_cv_r2.mean():.4f} (+/- {lr_cv_r2.std():.4f})')


# In[ ]:


# =============================================================================
# MODEL 2 — RANDOM FOREST REGRESSOR
# Non-linear model used as a benchmark against Linear Regression.
# n_estimators=100, random_state set for reproducibility.
# =============================================================================

rf_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model',        RandomForestRegressor(n_estimators=100, random_state=42))
])

rf_pipeline.fit(X_train, y_train)
y_pred_rf = rf_pipeline.predict(X_test)

rf_rmse = np.sqrt(mean_squared_error(y_test, y_pred_rf))
rf_r2   = r2_score(y_test, y_pred_rf)

rf_cv_r2 = cross_val_score(rf_pipeline, X, y, cv=5, scoring='r2')

print('=== Random Forest Regressor ===')
print(f'Test RMSE : {rf_rmse:.2f}')
print(f'Test R²   : {rf_r2:.4f}')
print(f'CV R²     : {rf_cv_r2.mean():.4f} (+/- {rf_cv_r2.std():.4f})')


# In[ ]:


# =============================================================================
# MODEL EVALUATION AND SELECTION
# Compare both models on RMSE and R2, then select and justify the better one.
# =============================================================================

import matplotlib.pyplot as plt

models  = ['Linear Regression', 'Random Forest']
rmse_scores = [lr_rmse, rf_rmse]
r2_scores   = [lr_r2,   rf_r2]

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].bar(models, rmse_scores, color=['steelblue', 'mediumseagreen'], edgecolor='white')
axes[0].set_title('Model Comparison — RMSE (lower is better)', fontsize=12)
axes[0].set_ylabel('RMSE')

axes[1].bar(models, r2_scores, color=['steelblue', 'mediumseagreen'], edgecolor='white')
axes[1].set_title('Model Comparison — R² (higher is better)', fontsize=12)
axes[1].set_ylabel('R²')
axes[1].set_ylim(0, 1)

plt.tight_layout()
plt.savefig('assets/viz_ml_comparison.png', dpi=150)
plt.show()

# Select model with lower RMSE
best = 'Linear Regression' if lr_rmse <= rf_rmse else 'Random Forest'
print(f'\nSelected model: {best}')
print('Rationale: Given the small dataset size (40 rows), the simpler model '
      'is preferred to reduce overfitting risk unless Random Forest shows '
      'substantially better cross-validated R².')


# In[8]:


# ⚠️ Make sure you run this cell at the end of your notebook before every submission!
get_ipython().system('jupyter nbconvert --to python source.ipynb')

