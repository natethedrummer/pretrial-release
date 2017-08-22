# import packages
import numpy as np
import pandas as pd
from ImportData import get_offenses
import statsmodels.api as sm
import statsmodels.formula.api as smf

# get data frame of felony offenses and release status
df = get_offenses()

df = df[np.isfinite(df['Bond Amount'])]
df = df[df['Bond Amount'] > 0]
df['bond_amount_ln'] = np.log(df['Bond Amount'])

df = df[df['Age'] != "#VALUE!"]
df['Age'] = df['Age'].astype(float)

df = df[['SPN 2','bond_amount_ln', 'F1', 'F2', 'F3', 'FC', 'family_offense', 'dwi_offense', 'prior_felony', 'prior_misdemeanor',
    'hired_attorney', 'black', 'hispanic', 'female', 'Age']]


 
# ols results of natural log of bond amount

# model 1: felony class, family, dwi, priors (yes/no)
results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony + prior_misdemeanor', data=df).fit()
print(results.summary())

# model 2: felony class, family, dwi, priors (yes/no), privateatt, black, hispanic, female, age
results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony + prior_misdemeanor + hired_attorney + black + hispanic + female + Age', data=df).fit()
print(results.summary())

# coefficient, standard error, sig at 0.10, 0.05, or 0.01
# count
# F-stat w/ p-value
# r-squared and adj r-squared

# estimate coefficients and odds ratio of logit equation: probability of bail

# estimated probability of bail for selected defendant types


