# import packages
import pandas as pd

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
    
    return df_offenses

# test
if __name__ == "__main__":
   
    df = get_offenses()

    print(df.columns)

    print(df.head())
