import pandas as pd
import numpy as np
import os

from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

from sklearn.linear_model import LogisticRegression
from math import exp
import pickle


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
    skewed = skewed_columns[skewed_columns]
    
    for col in skewed.keys():
        data_scores[col] = np.log(1.0 + data_scores[col])
    
    fattail_columns = (stats['skew'] > skew_threshold) & (stats['min'] < 0.0)
    fattail = fattail_columns[fattail_columns]
    
    for col in fattail.keys():
        data_scores[col] = np.log(
            data_scores[col] + 
            np.sqrt(np.power(data_scores[col],2) + 1.0))
    
    mean_vals = data_scores.mean()
    std_vals = data_scores.std()
    
    data_scores = (data_scores-mean_vals)/std_vals
    
    data_scores['is_churn'] = churn_data['is_churn']
    data_scores
    
    data_scores.to_csv("Generated/scores.csv",header=True)

    print(skewed_columns)
    print(fattail_columns)
    print(mean_vals)
    print(std_vals)
    
    score_params_df = pd.DataFrame(
        {
            'skew_score':skewed_columns,
            'fattail_score':fattail_columns,
            'mean':mean_vals,
            'std':std_vals
        },index=skewed_columns.index
    )

    print(score_params_df)
    
    score_params_df.to_csv('Generated/score_params.csv')

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


def ApplyLoadingMatrix():
    score_data = pd.read_csv('Generated/scores.csv', index_col=[0,1])
    
    data_2group = score_data.drop('is_churn',axis=1)

    load_mat_df = pd.read_csv('Generated/load_matrix.csv', index_col=[0])

    load_mat_ndarray = load_mat_df.to_numpy()

    ndarray_2group = data_2group[load_mat_df.index.values].to_numpy()
    
    grouped_ndarray = np.matmul(
        ndarray_2group,
        load_mat_ndarray
    )

    churn_data_grouped = pd.DataFrame(
        grouped_ndarray, 
        columns=load_mat_df.columns.values, 
        index=score_data.index
    )

    churn_data_grouped['is_churn'] = score_data['is_churn']
    churn_data_grouped

    churn_data_grouped.to_csv('Generated/groupscore.csv')
    

def LogisticRegressionAnalysis():
    grouped_data = pd.read_csv('Generated/groupscore.csv',index_col=[0,1])
    grouped_data

    y = grouped_data['is_churn'].astype(np.bool)
    #is retention 
    y = ~y
    
    y

    X = grouped_data.drop(['is_churn'], axis=1)
    X

    #lasso regression l1
    #automatic feature selection
    
    retain_reg = LogisticRegression(fit_intercept=True, solver='liblinear', penalty='l1')
    retain_reg.fit(X, y)

    def s_curve(x):
        return 1.0 / (1.0 + np.exp(-x))
        
    
    #bias term predicted
    average_retain = s_curve(retain_reg.intercept_)
    average_retain
    
    one_stdev_retains = np.array([
        s_curve(retain_reg.intercept_ + c) for c in retain_reg.coef_[0]
    ])
    
    one_stdev_impact = one_stdev_retains - average_retain
    
    average_retain
    one_stdev_impact

    group_lists = pd.read_csv('Generated/groupmets.csv', index_col=0)
    group_lists

    
    coef_df = pd.DataFrame.from_dict(
        {
            'group_metric_offset':np.append(group_lists.index, 'offset'),
            'weight': np.append(retain_reg.coef_[0],retain_reg.intercept_),
            'retain_impact': np.append(one_stdev_impact, average_retain),
            'group_metrics': np.append(group_lists['metrics'],'baseline')
        }
    )
    coef_df

    coef_df.sort_values(by=['weight'],ascending=False, inplace=True)
    coef_df.to_csv('Generated/logreg_summary.csv',index=False)

    with open('Generated/model.pkl', 'wb') as fid:
        print(fid)
        pickle.dump(retain_reg, fid)


    predictions = retain_reg.predict_proba(X)
    retain_reg.classes_

    predict_df = pd.DataFrame(predictions, index=X.index, columns=['churn_prob','retain_prob'])
    predict_df

    predict_df.to_csv("Generated/predictions.csv", header=True)
    


GenerateStats('Generated/original.csv')
ScoreData()
GenerateStats('Generated/scores.csv')
CreateLoadingMatrix()
ApplyLoadingMatrix()
LogisticRegressionAnalysis()

