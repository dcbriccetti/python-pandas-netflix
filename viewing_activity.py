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
    svt = 'Supplemental Video Type'
    df: DataFrame = pd.read_csv(
        REPORT_DIR + 'CONTENT_INTERACTION/ViewingActivity.csv', index_col='Title',
        usecols=['Title', 'Start Time', 'Duration', svt], parse_dates=['Start Time']) \
        .fillna('') \
        .rename(columns={svt: 'Type'})
    df['Duration'] = pd.to_timedelta(df['Duration'])
    return df.sort_values(by='Start Time')

config_display()
df = create_dataframe()
mdf = get_title_matches('Seinfeld', df)
print(mdf, '\n')
print(Fore.LIGHTYELLOW_EX + 'Total watch time:', mdf['Duration'].sum())
