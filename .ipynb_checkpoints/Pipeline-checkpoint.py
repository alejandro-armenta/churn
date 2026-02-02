import pandas as pd
import numpy as np
import os

#GET STATISTICS

def GenerateStats(path_file):
    #i = 'Generated/original.csv'
    i = path_file
    churn_data = pd.read_csv(i, index_col=[0,1])
    
    churn_data['is_churn'] = churn_data['is_churn'].astype(float)
    #print(churn_data)
    summary = churn_data.describe()
    summary = summary.transpose()
    summary['skew'] = churn_data.skew()
    summary['1%'] = churn_data.quantile(q=0.01)
    summary['99%'] = churn_data.quantile(q=0.99)
    summary['nonzero'] = churn_data.astype(bool).sum(axis=0) / churn_data.shape[0]
    summary = summary[['count','nonzero','mean','std','skew','min','1%','25%','50%','75%','99%','max']]
    summary.columns = summary.columns.str.replace("%", " pct")
    print(i.split('.')[0])
    summary.to_csv(i.split('.')[0] + '_stats.csv', header=True)

GenerateStats('Generated/original.csv')

#SCORE DATA

churn_data = pd.read_csv('Generated/original.csv', index_col=[0,1])
churn_data

data_scores = churn_data.copy()
data_scores = data_scores.drop('is_churn', axis=1)
data_scores

stats = pd.read_csv('Generated/original_stats.csv', index_col=0)
stats

stats = stats.drop('is_churn', axis=0)

#estas son las normales
skew_threshold = 2.8
skewed_columns = (stats['skew'] > skew_threshold) & (stats['min'] >= 0.0)
skewed_columns = skewed_columns[skewed_columns]
skewed_columns

for col in skewed_columns.keys():
    data_scores[col] = np.log(1.0 + data_scores[col])

fattail_columns = (stats['skew'] > skew_threshold) & (stats['min'] < 0.0)
fattail_columns = fattail_columns[fattail_columns]
fattail_columns

for col in fattail_columns.keys():
    data_scores[col] = np.log(
        data_scores[col] + 
        np.sqrt(np.power(data_scores[col],2) + 1.0))

mean_vals = data_scores.mean()
std_vals = data_scores.std()
#mean_vals.at['like_per_month']
#mean_vals.at['account_tenure']

data_scores = (data_scores-mean_vals)/std_vals

data_scores['is_churn'] = churn_data['is_churn']
data_scores

data_scores.to_csv("Generated/scores.csv",header=True)

pd.DataFrame(
    {
        'skew_score':skewed_columns,
        'fattail_score':fattail_columns,
        'mean':mean_vals,
        'std':std_vals
    }
).to_csv('Generated/score_params.csv', header=True)

GenerateStats('Generated/scores.csv')