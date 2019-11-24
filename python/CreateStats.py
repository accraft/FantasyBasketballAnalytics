import pandas as pd
import re
from sqlalchemy import create_engine
#import dfgui #not required, but useful to view dataframes
pd.options.display.max_colwidth = 150

#read in file
def read_in_file(csv_path):
    return pd.DataFrame.from_csv(csv_path, header=0,index_col=None)

#create function to extract week
def extract_week(week_string):
    if type(week_string) is str:
        weeksearch = re.search("( [0-9] )|( [0-9][0-9] )",week_string)
        return int(weeksearch.group(0).strip())

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
#acie_score_week_1 = DF_AllScores.loc[(DF_AllScores['Matchup Number'] == 1) & (DF_AllScores['WEEK_NUM'] == 1),:].iloc[[0]]
#acie_opponent_week_1 = DF_AllScores.loc[(DF_AllScores['Matchup Number'] == 1) & (DF_AllScores['WEEK_NUM'] == 1)].iloc[[1]]
#calculate_scores(acie_score_week_1,acie_opponent_week_1,result_only=False)
#calculate_scores(acie_score_week_1,acie_opponent_week_1,result_only=True)

#assign W/L to each game
def W_L_Calculation_Loop(df_to_loop_over):
    W_L_Calculation = []
    for row in df_to_loop_over.itertuples(index=False):
        W_L_Calculation.append(calculate_scores
                        (DF_AllScores.loc[(df_to_loop_over['Matchup Number'] == row.__getattribute__('_1'))
                                        & (df_to_loop_over['WEEK_NUM'] == row.__getattribute__('WEEK_NUM'))
                                        & (df_to_loop_over['NAME'] == row.__getattribute__('NAME')), :]
                        ,DF_AllScores.loc[(df_to_loop_over['Matchup Number'] == row.__getattribute__('_1'))
                                        & (df_to_loop_over['WEEK_NUM'] == row.__getattribute__('WEEK_NUM'))
                                        & (df_to_loop_over['NAME'] != row.__getattribute__('NAME')), :]
                        ,result_only=True))
    return W_L_Calculation



def main():
    DF_AllScores = read_in_file('C:\\Users\\accra_000\\PycharmProjects\\AnalyseBBallLeague\\all_scores.csv')
    DF_AllScores['WEEK_NUM'] = DF_AllScores['Week Name'].apply(extract_week)  # apply function over dataframe
    DF_AllScores = DF_AllScores.assign(Week_WL=W_L_Calculation_Loop(DF_AllScores))

    # finally upload the whole thing to a Postgresql environment
    engine = create_engine('postgresql://ac_craft:lobsterhoops@mybballstats.cogao6xb2eii.us-east-1.rds.amazonaws.com:5432/general_stats')
    DF_AllScores = DF_AllScores.rename(index=str, columns={u'FG%': "FGP", u'FT%': "FTP"})
    DF_AllScores.to_sql('weekly_scores', engine, chunksize=1000)

if __name__ == '__main__':
    main()


