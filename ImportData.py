# import packages
import pandas as pd
import numpy as np

# get offenses
def get_offenses():

    # import Felony Master Database clean excel spreadsheet
    path_fmd = "https://raw.github.com/natethedrummer/pretrial-release/master/felony_offenses.csv"
    df = pd.read_csv(path_fmd)

    # made bail
    df.rename(columns={'access': 'made_bail'}, inplace=True)
 
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

    df['offense_bin'] = df['Offense'].map(series_offense)
    
    # binary offense variables
    offense_list = df['offense_bin'].unique().tolist()
    for offense in offense_list:
        series = pd.Series({offense: 1})
        df[offense] = df['offense_bin'].map(series)
        df[offense].fillna(value=0, inplace=True)

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
 
    # prior misdemeanors
    df.rename(columns={'Misd priors': 'prior_misdemeanors'}, inplace=True)
   
    # prior misdemeanor (yes/no)
    df['prior_misdemeanor'] = np.where(df['prior_misdemeanors']>=1, 1, 0)

    # prior felonies
    df.rename(columns={'felony priors': 'prior_felonies'}, inplace=True)
    
    # prior felony (yes/no)
    df['prior_felony'] = np.where(df['prior_felonies']>=1, 1, 0)

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
 
    # white
    series = pd.Series({'WHITE': 1})
    df['white'] = df['race'].map(series)
    df['white'].fillna(value=0, inplace=True)
   
    # female
    series = pd.Series({'F': 1})
    df['female'] = df['gender'].map(series)
    df['female'].fillna(value=0, inplace=True)
   
    # male
    series = pd.Series({'M': 1})
    df['male'] = df['gender'].map(series)
    df['male'].fillna(value=0, inplace=True)

    print(df.groupby('HCJ Booked').count())
    return df

