# import packages
import numpy as np
import pandas as pd 


# create bail stats table
def bail_stats(df):

    # disposed cases only
    df = df[df['CASE DISPOSED STATUS'] == 'DISPOSED']
 
    # bail amount    
    df[~(df['BOND $'] == 'NO BOND')]    
    df['bail_amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)

    # age 
    df = df[df['age'] != "#VALUE!"]
    df['age'] = df['age'].astype(float)
  
    # select features    
    df = df[['made_bail',
                'bail_amount',
                'prior_felonies',
                'prior_misdemeanors',
                'hired_attorney',
                'age',
                'FC',
		'F1',
		'F2',
		'F3',
		'FS',
		'prior_misdemeanor',
		'prior_felony',
		'dwi_offense',
		'family_offense',
		'male',
		'black',
		'hispanic']]
  
    # produce summary statistics
    df = df.describe()
    
    # include count, mean and standard deviation only
    df = df.ix[['count','mean','std']]

    # transpose
    df = df.transpose()

    # rename index as Variable
    df.index.name = 'Variable'

    # rename stats
    df.rename(columns={'count': 'N',
        'mean': 'Mean or Percent',
        'std': 'Standard Deviation'
        }, inplace=True)

    # output to csv
    df.to_csv('bail_stats.csv')


# define bail_amount_by_demographic
def bail_amount_stats(df):

    # create frames list
    frames = []

    # disposed cases only
    df = df[df['CASE DISPOSED STATUS'] == 'DISPOSED']

    # select features    
    df = df[['BOND $',
               'gender',
                'race',
                'age']]
    # bail amount    
    df[~(df['BOND $'] == 'NO BOND')]    
    df['Bail Amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)
    df.drop('BOND $', axis=1, inplace=True)

    # rename gender to sex
    df.rename(columns={'gender': 'sex'}, inplace=True)

    # get average bail amount by sex and age
    bins = [0, 20, 30, 45, 100]
    
    group_names = ['Under 20',
	'Twenties',
	'30 to 45',
	'Over 45']

    df = df[df['age'] != "#VALUE!"]

    df['age'] = df['age'].astype(float)
 
    df['age category'] = pd.cut(df['age'], bins, labels=group_names)

    df_frame = df['Bail Amount'].groupby([df['age category'], df['sex']]).describe()

    frames.append(df_frame)

    # create demographics list
    demographics = ['sex','race']

    # get average bail amount by demographics
    for d in demographics:

        df_frame = df['Bail Amount'].groupby(df[d]).describe()

        frames.append(df_frame)

    i=0
 
    for f in frames:

        print(f)

        df = f
        
        # include count and mean only
        df = df[['count','mean']]

        # rename stats
        df.rename(columns={'count': 'N',
            'mean': 'Mean'
            }, inplace=True)

        # output to excel
        df.to_csv('bail_amount_stats_' + str(i) + '.csv')
       
        i+=1


def ptr_stats(df):

    df = df[['CASE DISPOSED STATUS','HCJ Booked','MADE Y / N','PRETRIAL STATUS AT DISPOSITION','bail type made simple']] 

    crosstab = pd.crosstab([df['CASE DISPOSED STATUS'],df['HCJ Booked'],df['MADE Y / N'],df['PRETRIAL STATUS AT DISPOSITION']], df['bail type made simple'],  margins=True)

    print(crosstab)

    crosstab.to_csv('ptr_stats.csv')
