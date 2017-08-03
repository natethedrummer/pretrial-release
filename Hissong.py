import pandas as pd 

# create descriptive statistics table
def descriptive_stats(df_offenses):

    # disposed cases only
    df = df_offenses[df_offenses['CASE DISPOSED STATUS'] == 'DISPOSED']
    
    # select features    
    df = df[['access',
                'BOND $',
                'felony priors',
                'Misd priors',
                'offense_bin',
                'hired_attorney',
                'gender',
                'race',
                'age']]
    
    # made bail
    df.rename(columns={'access': 'made_bail'}, inplace=True)
    
    # prior misdemeanors
    df.rename(columns={'Misd priors': 'prior_misdemeanors'}, inplace=True)
    
    # prior felonies
    df.rename(columns={'felony priors': 'prior_felonies'}, inplace=True)
    
    # bond amount    
    df[~(df['BOND $'] == 'NO BOND')]    
    df['bond_amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)
    df.drop('BOND $', axis=1, inplace=True)
    
    # dwi
    series = pd.Series({'DWI': 1})
    df['dwi'] = df['offense_bin'].map(series)
    df['dwi'].fillna(value=0, inplace=True)
    
    # retained private attorney
    df.rename(columns={'hired_attorney': 'private_attorney'}, inplace=True)
    
    # male
    series = pd.Series({'M': 1})
    df['male'] = df['gender'].map(series)
    df['male'].fillna(value=0, inplace=True)
    df.drop('gender', axis=1, inplace=True)
    
    # black
    series = pd.Series({'BLACK': 1})
    df['black'] = df['race'].map(series)
    df['black'].fillna(value=0, inplace=True)
    df.groupby('race').count()
    
    # hispanic
    series = pd.Series({'HISPANIC': 1})
    df['hispanic'] = df['race'].map(series)
    df['hispanic'].fillna(value=0, inplace=True)
    df.drop('race', axis=1, inplace=True)
    
    df = df.describe()
    df.index.name = 'variable'
    
    # output to excel
    writer = pd.ExcelWriter('descriptive_statistics.xlsx')
    df.to_excel(writer, 'Sheet1')
    writer.save()
    
    return df
