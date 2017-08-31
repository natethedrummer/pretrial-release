# import packages
import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

def model_bail_amount(df):

	# subset to disposed cases only
	df = df[df['CASE DISPOSED STATUS'] == 'DISPOSED']

	# clean age data 
	df = df[df['age'] != "#VALUE!"]
	df['age'] = df['age'].astype(float)

	# clean bail amount data    
	df[~(df['BOND $'] == 'NO BOND')]    
	df['bail_amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)

	# transform bail amount using natural log
	df = df[np.isfinite(df['bail_amount'])]
	df = df[df['bail_amount'] > 0]
	df['bail_amount_ln'] = np.log(df['bail_amount'])

	print(df.groupby('HCJ Booked').count())


        # model 1: felony class, family, dwi, priors (yes/no)
	results = smf.ols('bail_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('model_bail_amount1.csv', 'w')
	csv.write(csv_summary)

	# model 2: felony class, family, dwi, priors (yes/no), privateatt, black, hispanic, female, age
	results = smf.ols('bail_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felony + hired_attorney + black + hispanic + female + age', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('model_bail_amount2.csv', 'w')
	csv.write(csv_summary)

def model_ptr(df):

	# subset to disposed cases only
	df = df[df['CASE DISPOSED STATUS'] == 'DISPOSED']

	# clean bail amount data
	df[~(df['BOND $'] == 'NO BOND')]    
	df['bail_amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)

	# transform bail amount	using natural log
	df = df[np.isfinite(df['bail_amount'])]
	df = df[df['bail_amount'] > 0]
	df['bail_amount_ln'] = np.log(df['bail_amount'])

	# model probability of making bail
	results = smf.logit('made_bail ~ bail_amount_ln + hired_attorney + prior_felony + black + hispanic + female', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('model_ptr.csv', 'w')
	csv.write(csv_summary)

	# do scenario analysis of FS defendants
	df = df[df['FS'] == 1]
	df = df[['bail_amount_ln', 'hired_attorney', 'prior_felony', 'black', 'hispanic', 'female']]
	scenarios = pd.read_csv('predict_ptr.csv', usecols=['scenario','hired_attorney','prior_felony','black','hispanic','female'])      
	df = pd.merge(df, scenarios, how='inner', on=['hired_attorney','prior_felony','black','hispanic','female'])
	df.reset_index(inplace=True)
	df.drop('index', axis=1, inplace=True) 
	df.set_index(['scenario'], inplace=True)
	df['black'] = df['black'].astype(int)
	df['hispanic'] = df['hispanic'].astype(int)
	df['female'] = df['female'].astype(int)
	df = df.groupby(df.index).mean()
	prob = results.predict(df)
	df['prob'] = prob
	df['FS'] = 1
	df['bail_amount'] = np.exp(df['bail_amount_ln'])
	print(df)
	df.to_csv('predict_ptr.csv')

