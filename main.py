# import packages
from ImportData import get_offenses
from DescribeData import descriptive_stats, bail_amount_by_demographic, bail_status_tree 
from ModelData import explain_bond_amount, explain_made_bail


# get data frame of felony offenses and release status
df = get_offenses()


# bail status tree
bail_status_tree(df)


# descriptive statistics and mean bail amount
descriptive_stats(df)


# mean bail amount by demographics
bail_amount_by_demographic(df)


# ols results of natural log of bond amount
explain_bond_amount(df)


# estimate coefficients and odds ratio of logit equation: probability of bail
explain_made_bail(df)


# estimated probability of bail for selected defendant types


