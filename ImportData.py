# import packages
import pandas as pd
import numpy as np

# get offenses
def get_offenses():

    # import Felony Master Database clean excel spreadsheet
    path_fmd = "https://raw.github.com/natethedrummer/pretrial-release/master/felony_offenses.csv"
    df_offenses = pd.read_csv(path_fmd)

    # bin offense
    series_offense = pd.Series({'ARSON': 'ARSON',
                              'SALE DRUG': 'DRUG',
                              'POSS DRUG': 'DRUG',
                              'FEL DWI': 'DWI',
                              'KIDNAPPING': 'KIDNAPPING',
                              'CAP MURDER': 'MURDER',
                              'CAPITAL MURDER': 'MURDER',
                              'ASLT-MURDR': 'MURDER',
                              'MURD/MANSL': 'MURDER',
                              'MURDER': 'MURDER',
                              'ROBBERY': 'ROBBERY',
                              'THEFT': 'ROBBERY',
                              'BURGLARY': 'ROBBERY',
                              'burglary': 'ROBBERY',
                              'AUTO THEFT': 'ROBBERY',
                              'RAPE': 'SEX ABUSE',
                              'SEX ABUSE': 'SEX ABUSE',
                              'OTHER FEL': 'OTHER',
                              'OTHERMISD': 'OTHER'})

    df_offenses['offense_bin'] = df_offenses['Offense'].map(series_offense)
    
    # binary offense variables
    offense_list = df_offenses['offense_bin'].unique().tolist()
    for offense in offense_list:
        series = pd.Series({offense: 1})
        df_offenses[offense] = df_offenses['offense_bin'].map(series)
        df_offenses[offense].fillna(value=0, inplace=True)

    df = df_offenses

    # FC Offense
    df['FC'] = np.where(df['OffenseClass']=='FC', 1, 0)    

    # F1 Offense
    df['F1'] = np.where(df['OffenseClass']=='F1', 1, 0)    
    
    # F2 Offense
    df['F2'] = np.where(df['OffenseClass']=='F2', 1, 0)    

    # F3 Offense
    df['F3'] = np.where(df['OffenseClass']=='F3', 1, 0)    

    # FS Offense
    df['FS'] = np.where(df['OffenseClass']=='FS', 1, 0)    
    
    # drop OffenseClass
    df.drop('OffenseClass', axis=1, inplace=True)

    # age
    df.rename(columns={'age': 'Age'}, inplace=True)
    
    # made bail
    df.rename(columns={'access': 'Made Bail'}, inplace=True)
    
    # prior misdemeanors
    df.rename(columns={'Misd priors': 'Number of Prior Misdemeanors'}, inplace=True)
   
    # prior misdemeanor (yes/no)
    df['prior_misdemeanor'] = np.where(df['Number of Prior Misdemeanors']>=1, 1, 0)

    # prior felonies
    df.rename(columns={'felony priors': 'Number of Prior Felonies'}, inplace=True)
    
    # prior felony (yes/no)
    df['prior_felony'] = np.where(df['Number of Prior Felonies']>=1, 1, 0)

    # bond amount    
    df[~(df['BOND $'] == 'NO BOND')]    
    df['Bond Amount'] = (df[~(df['BOND $'] == 'NO BOND')])['BOND $'].astype(float)
    df.drop('BOND $', axis=1, inplace=True)
    
    # dwi
    series = pd.Series({'DWI': 1})
    df['dwi_offense'] = df['offense_bin'].map(series)
    df['dwi_offense'].fillna(value=0, inplace=True)
    
    # family offense
    df['family_offense'] = df['OffenseDescription'].str.contains('fam|chil|kid', case=False, na=False)
    df['family_offense'] = df['family_offense'].astype(int)

    # black
    series = pd.Series({'BLACK': 1})
    df['black'] = df['race'].map(series)
    df['black'].fillna(value=0, inplace=True)
    
    # hispanic
    series = pd.Series({'HISPANIC': 1})
    df['hispanic'] = df['race'].map(series)
    df['hispanic'].fillna(value=0, inplace=True)
   
    # female
    series = pd.Series({'F': 1})
    df['female'] = df['gender'].map(series)
    df['female'].fillna(value=0, inplace=True)
 

    return df

# test
if __name__ == "__main__":
   
    df = get_offenses()

    print(df.columns)

    print(df.head())
