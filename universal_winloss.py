import pandas as pd
import re
from sqlalchemy import create_engine

def read_in_df(sql_query_torun):
    pg_un = raw_input("enter posgres user name")
    pg_pw = raw_input("enter posgres password")

    engine = create_engine('postgresql://'+pg_un+':'+pg_pw+'@mybballstats.cogao6xb2eii.us-east-1.rds.amazonaws.com:5432/general_stats')
    return pd.read_sql_query(sql_query_torun,engine)

#function to calculate score assuming the opponents scores are on the same row
def calculate_scores_samerow (matchup_row,result_only=True):
    score_cat_list = ['FGP','FTP','3PM','REB','AST','STL','BLK','TO','PTS']
    won_cats=0
    lost_cats=0
    tie_cats=0
    for item in score_cat_list:
        if (item != 'TO' and matchup_row[item] > matchup_row[item+"_opp"]) or (item == 'TO' and matchup_row[item] < matchup_row[item+"_opp"]):
            won_cats += 1
        elif (item != 'TO' and matchup_row[item] < matchup_row[item+"_opp"]) or (item == 'TO' and matchup_row[item] > matchup_row[item+"_opp"]):
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

#append a suffix to all columns columns
def append_suffix (df_base,suffix,exclude_list=[""]):
    df_base2 = df_base.copy()
    newcolumns = []
    for col in df_base2.columns:
        if str(col) not in exclude_list:
           newcolumns.append(str(col) + suffix)
        else:
           newcolumns.append(str(col))
    df_base2.columns = newcolumns
    return df_base2
#df_test  = pd.DataFrame([[1,2,3,4],[5,6,7,8]], columns=list('ABCD'))
#append_suffix (df_test,"suffix_test",["B","cat"])



#ac_craft
#[second word o' teamname NOT PLURAL][going to go shoot some XXXXX (plural)] - all lowercase
df_all_results = read_in_df("SELECT * FROM public.weekly_scores")
df_all_results2 = append_suffix(df_all_results,"_opp",exclude_list=["WEEK_NUM"])
#cartesian product
df_all_results_cartesian = df_all_results.merge(df_all_results2,on='WEEK_NUM',how='left')
#remove matches with self
df_all_results_cartesian = df_all_results_cartesian[(df_all_results_cartesian.NAME != df_all_results_cartesian.NAME_opp)]
#calculate the scores
df_all_results_cartesian['cartesian_WL'] = df_all_results_cartesian.apply(calculate_scores_samerow,1,result_only=False)
df_all_results_cartesian['cartesian_result'] = df_all_results_cartesian.apply(calculate_scores_samerow,1,result_only=True)
#back to row-level
cols_to_groupby = [x for x in df_all_results_cartesian.columns.values if "_opp" not in x]
gdf = df_all_results_cartesian.groupby(cols_to_groupby)

