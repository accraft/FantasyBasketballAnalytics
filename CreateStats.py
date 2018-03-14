import pandas as pd
import re
#import dfgui #not required, but useful to view dataframes

pd.options.display.max_colwidth = 150

#read in file, and extract the week number from the week
path = 'C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\all_scores.csv'
DF_AllScores = pd.DataFrame.from_csv(path, header=0,index_col=None)
#create function to extract week
def extract_week(week_string):
    if type(week_string) is str:
        weeksearch = re.search("( [0-9] )|( [0-9][0-9] )",week_string)
        return int(weeksearch.group(0).strip())
DF_AllScores['WEEK_NUM'] = DF_AllScores['Week Name'].apply(extract_week) #apply function over dataframe

#function to calculate score
def calculate_scores (matchup_row,opponent_row,result_only=True):
    score_cat_list = ['FG%','FT%','3PM','REB','AST','STL','BLK','TO','PTS']
    won_cats=0
    lost_cats=0
    tie_cats=0
    for item in score_cat_list:
        if (item != 'TO' and matchup_row[item].values > opponent_row[item].values) or (item == 'TO' and matchup_row[item].values < opponent_row[item].values):
            won_cats += 1
        elif (item != 'TO' and matchup_row[item].values < opponent_row[item].values) or (item == 'TO' and matchup_row[item].values > opponent_row[item].values):
            lost_cats +=1
        else:
            tie_cats +=1

    if won_cats > lost_cats:
        result=1
    elif won_cats < lost_cats:
        result=-1
    else:
        result=0

    if result_only:
        return result
    else:
        return str(won_cats)+'-'+str(lost_cats)+'-'+str(tie_cats)

#sample call
#acie_score_week_1 = DF_AllScores.loc[(DF_AllScores['NAME'] == u'The Dazzling Lobcity Stars (4-15)') & (DF_AllScores['WEEK_NUM'] == 1),:]
#acie_opponent_week_1 = DF_AllScores.loc[(DF_AllScores['Matchup Number'] == 1) & (DF_AllScores['WEEK_NUM'] == 1) & (DF_AllScores['NAME'] != u'The Dazzling Lobcity Stars (4-15)') ,:]
#calculate_scores(acie_score_week_1,acie_opponent_week_1,result_only=False)
#calculate_scores(acie_score_week_1,acie_opponent_week_1,result_only=True)

