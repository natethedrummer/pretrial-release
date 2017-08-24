# import packages
import statsmodels.api as sm
import statsmodels.formula.api as smf

def explain_bond_amount(df):

	# model 1: felony class, family, dwi, priors (yes/no)
	results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felonies + prior_misdemeanors', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('bond_model1.csv', 'w')
	csv.write(csv_summary)


	# model 2: felony class, family, dwi, priors (yes/no), privateatt, black, hispanic, female, age
	results = smf.ols('bond_amount_ln ~ F1 + F2 + F3 + FC + family_offense + dwi_offense + prior_felonies + prior_misdemeanors + hired_attorney + black + hispanic + female + age', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('bond_model2.csv', 'w')
	csv.write(csv_summary)


def explain_made_bail(df):

	# model
	results = smf.logit('made_bail ~ bond_amount_ln + hired_attorney + prior_misdemeanors + prior_felonies + black + hispanic + female', data=df).fit()
	print(results.summary())
	Summary = results.summary()
	csv_summary = Summary.as_csv()
	csv = open('made_bail_model.csv', 'w')
	csv.write(csv_summary)


