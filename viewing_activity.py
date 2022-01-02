'Analyze Netflix Viewing Activity (https://help.netflix.com/en/node/101917)'

import pandas as pd
from colorama import Fore

report_dir = '/Users/daveb/Documents/netflix-report/'
title_search = 'Seinfeld'

svt = 'Supplemental Video Type'
df = pd.read_csv(
    report_dir + 'CONTENT_INTERACTION/ViewingActivity.csv',
    index_col='Title',
    usecols=['Title', 'Start Time', 'Duration', svt],
    parse_dates=['Start Time']) \
    .fillna('') \
    .rename(columns={svt: 'Type'})
df['Duration'] = pd.to_timedelta(df['Duration'])

title_matches = df.index.str.contains(title_search)
sdf = df[title_matches].sort_values(by='Start Time')
for part in 'max_columns, min_rows, max_rows, width, max_colwidth'.split(', '):
    pd.set_option('display.' + part, None)
pd.set_option('display.max_rows', 35)
print(sdf, '\n')
print(Fore.LIGHTYELLOW_EX + 'Total watch time:', sdf['Duration'].sum())
