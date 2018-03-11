import pandas as pd
import re
import dfgui

import math

pd.options.display.max_colwidth = 150

#read in file, and add a name to the first column and extract the week number
path = 'C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\all_scores.csv'
DF_AllScores = pd.DataFrame.from_csv(path, header=0,index_col=None)
#create function to extract week
def extract_week(week_string):
    if type(week_string) is str:
        weeksearch = re.search("( [0-9] )|( [0-9][0-9] )",week_string)
        return int(weeksearch.group(0).strip())

DF_AllScores['WEEK_NUM'] = DF_AllScores['Week Name'].apply(extract_week)

# removes blank weeknumbers
DF_AllScores = DF_AllScores[DF_AllScores['WEEK_NUM'] == DF_AllScores['WEEK_NUM']]

DF_AllScores = DF_AllScores.drop(columns='WEEK')

DF_AllScores.head(1)

DF_AllScores[DF_AllScores['NAME'] == u'The Dazzling Lobcity Stars (3-10)']
DF_AllScores[['WEEK_NUM','NAME','PTS']]


dfgui.show(DF_AllScores)







