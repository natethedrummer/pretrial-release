# import packages
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

def explain_bond_amount(df):

	# prep data
	df = df[np.isfinite(df['bond_amount'])]
	df = df[df['bond_amount'] > 0]
	df['bond_amount_ln'] = np.log(df['bond_amount'])

	df = df[df['age'] != "#VALUE!"]
	df['age'] = df['age'].astype(float)

	df = df[['SPN 2','bond_amount_ln', 'F1', 'F2', 'F3', 'FC', 'family_offense', 'dwi_offense', 'prior_felony', 'prior_misdemeanor',
	    'hired_attorney', 'black', 'hispanic', 'female', 'age']]
	 
	# model 1: felony class, family, dwi, priors (yes/no)
	results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony + prior_misdemeanor', data=df).fit()
	print(results.summary())

	# model 2: felony class, family, dwi, priors (yes/no), privateatt, black, hispanic, female, age
	results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony + prior_misdemeanor + hired_attorney + black + hispanic + female + age', data=df).fit()
	print(results.summary())

	return None

