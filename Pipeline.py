import pandas as pd
import numpy as np
import os

from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

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


def ScoreData():
    
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

def CreateLoadingMatrix():
    score_data = pd.read_csv('Generated/scores.csv', index_col=[0,1])
    score_data
    score_data.drop('is_churn',axis=1, inplace=True)
    #estas son antes de ordenarlas
    metric_columns = list(score_data.columns.values)
    metric_columns

    group_corr_thresh = 0.5
    corr = score_data.corr()
    
    dissimilarity = 1.0 - corr
    diss_thresh = 1.0 - group_corr_thresh
    
    #entre mas chiquito menos distance matrix redundant
    dissimilarity

    #1D condensed distance matrix
    linkage_matrix = linkage(squareform(dissimilarity), method='single')

    labels = fcluster(
    linkage_matrix,diss_thresh,criterion='distance')

    labels

        #counts the number of elements on each cluster
    cluster_count = Counter(labels)
    
    #este diccionarion nadamas tiene los indices
    cluster_order = {cluster[0] : idx for idx, cluster in enumerate(cluster_count.most_common())}
    
    cluster_order

    relabeled_clusters = [cluster_order[l] for l in labels]

    relabeled_count = Counter(relabeled_clusters)
    relabeled_count

    relabeled_df = pd.DataFrame(
        {
            'group' : relabeled_clusters,
            'column' : metric_columns}).sort_values(['group','column'], ascending=[True,True])
    
    relabeled_df

    #originals X clusters
    load_mat = np.zeros((len(metric_columns), len(relabeled_count)))
    load_mat
    
    for row in relabeled_df.iterrows():
        #estas accediendo a la serie
        #print(row[1]['group']) - 0
        #print(row[1]['column']) - 1
        
        orig_col = metric_columns.index(row[1]['column'])
        if relabeled_count[row[1]['group']] > 1:
            load_mat[orig_col, row[1]['group']] = (
                1.0 / 
                (
                    np.sqrt(group_corr_thresh) * 
                    float(relabeled_count[row[1]['group']])
                )                                
            )
        else:
            load_mat[orig_col, row[1]['group']] = 1.0


    is_group = load_mat.astype(bool).sum(axis=0) > 1
    is_group

    column_names = [
        'metric_group_{}'.format(d) 
        if is_group[d] 
        else 
        relabeled_df.loc[relabeled_df['group'] == d, 'column'].item()
        for d in range(0,load_mat.shape[1])
    ]
    
    column_names    

    loadmat_df = pd.DataFrame(load_mat, index=metric_columns, columns=column_names)
    loadmat_df

    loadmat_df.to_csv('Generated/load_matrix.csv')

    group_lists = [
        '|'.join(relabeled_df[relabeled_df['group'] == g]['column']) 
        for g in set(relabeled_df['group'])
    ]
    
    group_lists

    groupmets = pd.DataFrame(group_lists, columns=['metrics'], index=loadmat_df.columns.values)
    groupmets

    groupmets.to_csv('Generated/groupmets.csv')





GenerateStats('Generated/original.csv')
ScoreData()
GenerateStats('Generated/scores.csv')
CreateLoadingMatrix()