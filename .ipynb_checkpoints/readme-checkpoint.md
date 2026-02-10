# Churn Forecasting

I worked in customer retention making churn prediction for customers.

I made different metrics for customers as:
                         
- like per month.
- newfriend per month.
- post per month.
- adview per month.
- dislike per month.
- unfriend per month.


|account_id          |observation_date    |is_churn            |like_per_month        |newfriend_per_month|post_per_month|adview_per_month|dislike_per_month|unfriend_per_month                                                                 |message_per_month |reply_per_month   |account_tenure    |adview_per_post     |reply_per_message|like_per_post     |post_per_message  |unfriend_per_newfriend|dislike_pcnt          |unfriend_per_newfriend_scaled|newfriend_pcnt_chng|days_since_newfriend|unfriend_28day_avg_84day_obs|unfriend_28day_avg_84day_obs_scaled|
|--------------------|--------------------|--------------------|----------------------|-------------------|--------------|----------------|-----------------|-----------------------------------------------------------------------------------|------------------|------------------|------------------|--------------------|-----------------|------------------|------------------|----------------------|----------------------|-----------------------------|-------------------|--------------------|----------------------------|-----------------------------------|
|27                  |2020-03-01          |False               |28.0                  |5.0                |14.0          |33.0            |2.0              |1.0                                                                                |1.0               |0.0               |55.0              |2.357143            |0.0              |2.0               |14.0              |0.2                   |0.06666667            |0.10181818                   |4.0                |3.0                 |0.33333334                  |0.5090909                          |
|51                  |2020-03-01          |False               |26.0                  |5.0                |4.0           |19.0            |4.0              |1.0                                                                                |42.0              |28.0              |55.0              |4.75                |0.6666667        |6.5               |0.0952381         |0.2                   |0.13333334            |0.20363636                   |-0.16666669        |1.0                 |0.6666667                   |1.0181818                          |
|95                  |2020-03-01          |False               |74.0                  |5.0                |64.0          |17.0            |20.0             |0.0                                                                                |12.0              |6.0               |55.0              |0.265625            |0.5              |1.15625           |5.3333335         |0.0                   |0.21276596            |0.0                          |0.25               |1.0                 |0.0                         |0.0                                |
|123                 |2020-03-01          |False               |28.0                  |6.0                |13.0          |4.0             |25.0             |0.0                                                                                |11.0              |1.0               |55.0              |0.30769232          |0.09090909       |2.1538463         |1.1818181         |0.0                   |0.4716981             |0.0                          |1.0                |2.0                 |0.0                         |0.0                                |
|189                 |2020-03-01          |True                |3.0                   |1.0                |8.0           |16.0            |2.0              |0.0                                                                                |0.0               |0.0               |55.0              |2.0                 |0.0              |0.375             |0.0               |0.0                   |0.4                   |0.0                          |0.0                |15.0                |0.0                         |0.0                                |
|331                 |2020-03-01          |False               |193.0                 |7.0                |12.0          |25.0            |1.0              |0.0                                                                                |11.0              |6.0               |55.0              |2.0833333           |0.54545456       |16.083334         |1.0909091         |0.0                   |0.005154639           |0.0                          |1.3333333          |0.0                 |0.0                         |0.0                                |
|352                 |2020-03-01          |False               |10.0                  |2.0                |5.0           |3.0             |4.0              |0.0                                                                                |3.0               |0.0               |55.0              |0.6                 |0.0              |2.0               |1.6666666         |0.0                   |0.2857143             |0.0                          |1.0                |1.0                 |0.0                         |0.0                                |
|374                 |2020-03-01          |False               |333.0                 |10.0               |273.0         |114.0           |30.0             |0.0                                                                                |98.0              |34.0              |55.0              |0.41758242          |0.3469388        |1.2197802         |2.7857144         |0.0                   |0.08264463            |0.0                          |0.42857146         |7.0                 |0.0                         |0.0                                |
|419                 |2020-03-01          |False               |87.0                  |4.0                |28.0          |93.0            |20.0             |0.0                                                                                |11.0              |2.0               |55.0              |3.3214285           |0.18181819       |3.107143          |2.5454545         |0.0                   |0.18691589            |0.12727273                   |3.0                |0.0                 |0.33333334                  |0.5090909                          |
|421                 |2020-03-01          |False               |251.0                 |26.0               |144.0         |251.0           |57.0             |1.0                                                                                |26.0              |14.0              |55.0              |1.7430556           |0.53846157       |1.7430556         |5.5384617         |0.03846154            |0.18506494            |0.01958042                   |0.13043475         |1.0                 |0.33333334                  |0.5090909                          |


This is the pipeline for dataset generation:

![ale](Cohorts/pipeline.png)



I made feature engineering for metrics about customers' events and subscriptions:


                           
This is a forcasting model for churn prediction.

![ale](crossval_regression.png)

I made hyper parameter tuning with cross validation:

The hyperparameters tuned were:

- learning rate 
- max_depth
- min child weight
- number of estimators

This is the result for the best XGBoost model which has 0.7196238811183722 of ROC_AUC:

Here you can look at the best model with the hyperparameters chosen:

|mean_fit_time       |std_fit_time        |mean_score_time     |std_score_time        |param_learning_rate|param_max_depth|param_min_child_weight|param_n_estimators|params                                                                             |split0_test_lift  |split1_test_lift  |mean_test_lift    |std_test_lift       |rank_test_lift|split0_test_AUC   |split1_test_AUC   |mean_test_AUC     |std_test_AUC          |rank_test_AUC|
|--------------------|--------------------|--------------------|----------------------|-------------------|---------------|----------------------|------------------|-----------------------------------------------------------------------------------|------------------|------------------|------------------|--------------------|--------------|------------------|------------------|------------------|----------------------|-------------|
|0.07287085056304932 |0.020963311195373535|0.01981055736541748 |0.0018919706344604492 |0.4                |1              |6                     |120               |{'learning_rate': 0.4, 'max_depth': 1, 'min_child_weight': 6, 'n_estimators': 120} |3.458250865907966 |3.847048300536673 |3.6526495832223196|0.19439871731435354 |72            |0.7137452017660535|0.7255025604706908|0.7196238811183722|0.005878679352318672  |1            |



