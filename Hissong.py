# import packages
import numpy as np
import pandas as pd 
from ImportData import get_offenses

# create descriptive statistics table
def descriptive_stats(df_offenses):

    # disposed cases only
    df = df_offenses[df_offenses['CASE DISPOSED STATUS'] == 'DISPOSED']
    
    # select features    
    df = df[['access',
                'BOND $',
                'felony priors',
                'Misd priors',
                'OffenseDescription',
                'offense_bin',
      		'OffenseClass',
                'hired_attorney',
                'gender',
                'race',
                'age']]
    
    # FC Offense
    df['FC Offense'] = np.where(df['OffenseClass']=='FC', 1, 0)    

    # F1 Offense
    df['F1 Offense'] = np.where(df['OffenseClass']=='F1', 1, 0)    
    
    # F2 Offense
    df['F2 Offense'] = np.where(df['OffenseClass']=='F2', 1, 0)    

    # F3 Offense
    df['F3 Offense'] = np.where(df['OffenseClass']=='F3', 1, 0)    

    # FS Offense
    df['FS Offense'] = np.where(df['OffenseClass']=='FS', 1, 0)    
    
    # drop OffenseClass
    df.drop('OffenseClass', axis=1, inplace=True)

    # age
    df.rename(columns={'age': 'Age'}, inplace=True)
    
    # made bail
    df.rename(columns={'access': 'Made Bail'}, inplace=True)
    
    # prior misdemeanors
    df.rename(columns={'Misd priors': 'Number of Prior Misdemeanors'}, inplace=True)
   
    # prior misdemeanor (yes/no)
    df['Prior Misdemeanor (Yes/No)'] = np.where(df['Number of Prior Misdemeanors']>=1, 1, 0)

    # prior felonies
    df.rename(columns={'felony priors': 'Number of Prior Felonies'}, inplace=True)
    
    # prior felony (yes/no)
    df['Prior Felony (Yes/No)'] = np.where(df['Number of Prior Felonies']>=1, 1, 0)

    # bond amount    
    df[~(df['BOND $'] == 'NO BOND')]    
    df['Bond Amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)
    df.drop('BOND $', axis=1, inplace=True)
    
    # dwi
    series = pd.Series({'DWI': 1})
    df['DWI (Yes/No)'] = df['offense_bin'].map(series)
    df['DWI (Yes/No)'].fillna(value=0, inplace=True)
    
    # family offense
    df['Offense Against Family (Yes/No)'] = df['OffenseDescription'].str.contains('fam|chil|kid', case=False, na=False)
    df['Offense Against Family (Yes/No)'] = df['Offense Against Family (Yes/No)'].astype(int)

    # retained private attorney
    df.rename(columns={'hired_attorney': 'Retained Private Attorney (Yes/No)'}, inplace=True)
    
    # male
    series = pd.Series({'M': 1})
    df['Male (Yes/No)'] = df['gender'].map(series)
    df['Male (Yes/No)'].fillna(value=0, inplace=True)
    df.drop('gender', axis=1, inplace=True)
    
    # black
    series = pd.Series({'BLACK': 1})
    df['Black (Yes/No)'] = df['race'].map(series)
    df['Black (Yes/No)'].fillna(value=0, inplace=True)
    df.groupby('race').count()
    
    # hispanic
    series = pd.Series({'HISPANIC': 1})
    df['Hispanic (Yes/No)'] = df['race'].map(series)
    df['Hispanic (Yes/No)'].fillna(value=0, inplace=True)
    df.drop('race', axis=1, inplace=True)
   
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

    # output to excel
    writer = pd.ExcelWriter('descriptive_statistics.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    
    return df

# test
if __name__ == "__main__":

    df_offenses = get_offenses()

    df = descriptive_stats(df_offenses)

    print(df)

# define bail_amount_by_demographic
def bail_amount_by_demographic(df_offenses):

    # create frames list
    frames = []

    # disposed cases only
    df = df_offenses[df_offenses['CASE DISPOSED STATUS'] == 'DISPOSED']

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

    df['age category'] = pd.cut(df['age'], bins, labels=group_names)

    df_frame = df['Bail Amount'].groupby([df['age category'], df['sex']]).describe()

    frames.append(df_frame)

    # create demographics list
    demographics = ['sex','race']

    # get average bail amount by demographics
    for d in demographics:

        df_frame = df['Bail Amount'].groupby(df[d]).describe()

        frames.append(df_frame)

    # write each table to an Excel sheet
    writer = pd.ExcelWriter('bail_amount_by_demographic.xlsx')

    i=0
 
    for f in frames:

        df = f
        
        # include count and mean only
        df = df[['count','mean']]

        # rename stats
        df.rename(columns={'count': 'N',
            'mean': 'Mean'
            }, inplace=True)

        # output to excel
        df.to_excel(writer, 'Sheet' + str(i))
       
        i+=1

    writer.save()
 
# test
if __name__ == "__main__":

    df_offenses = get_offenses()

    bail_amount_by_demographic(df_offenses)
