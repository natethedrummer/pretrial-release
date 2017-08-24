# import packages
from ImportData import get_offenses
from DescribeData import descriptive_stats, bail_amount_by_demographic 
from ModelData import explain_bond_amount


# get data frame of felony offenses and release status
df = get_offenses()


# descriptive statistics and mean bail amount
descriptive_stats(df)


# mean bail amount by demographics
bail_amount_by_demographic(df)


# ols results of natural log of bond amount
explain_bond_amount(df)


# estimate coefficients and odds ratio of logit equation: probability of bail


# estimated probability of bail for selected defendant types


