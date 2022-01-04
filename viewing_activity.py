'Analyze Netflix Viewing Activity (https://help.netflix.com/en/node/101917)'

import pandas as pd
from pandas import DataFrame
from colorama import Fore

REPORT_DIR = '/Users/daveb/Documents/netflix-report/'

def config_display() -> None:
    'Show more rows and columns than the default'
    for part in 'max_columns, min_rows, max_rows, width, max_colwidth'.split(', '):
        pd.set_option('display.' + part, None)
    pd.set_option('display.max_rows', 35)

def get_title_matches(title_part: str, df: DataFrame) -> DataFrame:
    return df[df.index.str.contains(title_part)]

def create_dataframe():
    rename_col = ('Supplemental Video Type', 'Type')
    df: DataFrame = pd.read_csv(
        REPORT_DIR + 'CONTENT_INTERACTION/ViewingActivity.csv',
        index_col='Title',
        usecols=['Title', 'Start Time', 'Duration', rename_col[0]],
        parse_dates=['Start Time']) \
        .fillna('') \
        .rename(columns=dict([rename_col]))
    df['Duration'] = pd.to_timedelta(df['Duration'])
    df['Month'] = df['Start Time'].astype(str).str[:7]
    return df.sort_values(by='Start Time')

config_display()
df = create_dataframe()
mdf = get_title_matches('Seinfeld', df)
print(Fore.GREEN + '\nWatch time by type' + Fore.WHITE)
print(mdf.groupby('Type')[['Duration']].sum())
print(Fore.GREEN + '\nWatch time by month' + Fore.WHITE)
print(mdf.groupby('Month')[['Duration']].sum())
print(Fore.GREEN + '\nWatches by month' + Fore.WHITE)
print(mdf.groupby('Month')[['Duration']].count())
print(Fore.GREEN + '\nSessions' + Fore.WHITE)
print(mdf, '\n')
print(Fore.LIGHTYELLOW_EX + 'Total watch time:', mdf['Duration'].sum())
