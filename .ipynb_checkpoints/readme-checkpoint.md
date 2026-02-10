# Churn Forecasting

I worked in customer retention making churn prediction for customers.
                                                       
## SQL DATASET Generation
                                                       
I made different metrics from raw data of customer events and subscriptions. 

It is based on behavioral data and subscription data.

I used SQL for generating metrics and storing them into the database PostgreSQL.

This is the SQL for pivoting the data into a dataset for analysis.
           
```sql
--SQL for pivoting data in the database
                         
set search_path = 'socialnet7'; 

with observation_params as
(
    select  interval '7 day' as metric_period,
    '2020-03-01'::timestamp as obs_start,
    '2020-05-10'::timestamp as obs_end
)
select m.account_id, o.observation_date, is_churn,
sum(case when metric_name_id=0 then metric_value else 0 end) as like_per_month,
sum(case when metric_name_id=1 then metric_value else 0 end) as newfriend_per_month,
sum(case when metric_name_id=2 then metric_value else 0 end) as post_per_month,
sum(case when metric_name_id=3 then metric_value else 0 end) as adview_per_month,
sum(case when metric_name_id=4 then metric_value else 0 end) as dislike_per_month,
sum(case when metric_name_id=5 then metric_value else 0 end) as unfriend_per_month,
sum(case when metric_name_id=6 then metric_value else 0 end) as message_per_month,
sum(case when metric_name_id=7 then metric_value else 0 end) as reply_per_month,
sum(case when metric_name_id=8 then metric_value else 0 end) as account_tenure,

sum(case when metric_name_id=21 then metric_value else 0 end) as adview_per_post,
sum(case when metric_name_id=22 then metric_value else 0 end) as reply_per_message,
sum(case when metric_name_id=23 then metric_value else 0 end) as like_per_post,
sum(case when metric_name_id=24 then metric_value else 0 end) as post_per_message,
sum(case when metric_name_id=25 then metric_value else 0 end) as unfriend_per_newfriend,

sum(case when metric_name_id=27 then metric_value else 0 end) as dislike_pcnt,
sum(case when metric_name_id=28 then metric_value else 0 end) as unfriend_per_newfriend_scaled,

sum(case when metric_name_id=30 then metric_value else 0 end) as newfriend_pcnt_chng,
sum(case when metric_name_id=31 then metric_value else 0 end) as days_since_newfriend,
sum(case when metric_name_id=33 then metric_value else 0 end) as unfriend_28day_avg_84day_obs,
sum(case when metric_name_id=34 then metric_value else 0 end) as unfriend_28day_avg_84day_obs_scaled

from metric m inner join observation_params
on metric_time between obs_start and obs_end
inner join observation o on m.account_id = o.account_id
    and m.metric_time > (o.observation_date - metric_period)::timestamp
    and m.metric_time <= o.observation_date::timestamp
group by m.account_id, metric_time, observation_date, is_churn
order by observation_date,m.account_id;
```

And this is the result:

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


## Metric Statistics
                                                     
And these are the statistics of each metric. These statistics are used to normalize the metrics.
                                                     

|FIELD1|count                        |nonzero|mean                                         |std                |skew                 |min |1 pct|25 pct      |50 pct    |75 pct     |99 pct            |max      |
|------|-----------------------------|-------|---------------------------------------------|-------------------|---------------------|----|-----|------------|----------|-----------|------------------|---------|
|is_churn|25806.0                      |0.021235371619003334|0.021235371619003334                         |0.1441708571563562 |6.642143157207778    |0.0 |0.0  |0.0         |0.0       |0.0        |1.0               |1.0      |
|like_per_month|25806.0                      |0.991513601488026|94.32891575602574                            |205.78447933272324 |10.653469247257984   |0.0 |1.0  |16.0        |39.0      |93.0       |848.0             |6529.0   |
|newfriend_per_month|25806.0                      |0.8994807409129659|6.624002170037976                            |7.993498358467066  |3.66796146271989     |0.0 |0.0  |2.0         |4.0       |8.0        |39.0              |190.0    |
|post_per_month|25806.0                      |0.9819809346663566|38.93497636208634                            |71.60147703014306  |11.118123959680078   |0.0 |0.0  |8.0         |19.0      |43.0       |312.9500000000007 |3255.0   |
|adview_per_month|25806.0                      |0.9794621405874603|39.63961869332714                            |73.31706589120364  |8.866400160585089    |0.0 |0.0  |8.0         |19.0      |43.75      |325.9500000000007 |2067.0   |
|dislike_per_month|25806.0                      |0.9486166007905138|15.270712237464156                           |22.382892341521462 |6.233416663052152    |0.0 |0.0  |4.0         |9.0       |18.0       |102.0             |556.0    |
|unfriend_per_month|25806.0                      |0.261838332170813|0.3027202976052081                           |0.54855852163725   |1.7993781963865867   |0.0 |0.0  |0.0         |0.0       |1.0        |2.0               |4.0      |
|message_per_month|25806.0                      |0.9836084631481051|61.77896613190731                            |136.09371596158425 |8.460904583141067    |0.0 |0.0  |9.0         |24.0      |60.0       |596.0             |3751.0   |
|reply_per_month|25806.0                      |0.9142834999612494|22.561574827559483                           |47.47109529894967  |6.973424187785108    |0.0 |0.0  |2.0         |8.0       |22.0       |223.90000000000146|1310.0   |
|account_tenure|25806.0                      |1.0    |71.06510113926994                            |26.747373644961094 |-0.023286556783765216|18.0|19.0 |52.0        |80.0      |85.0       |116.0             |116.0    |
|adview_per_post|25806.0                      |0.9648143842517244|1.6243648138822133                           |2.41245582721761   |8.606037060617526    |0.0 |0.0  |0.4516129   |0.962963  |1.905137875|11.0              |101.0    |
|reply_per_message|25806.0                      |0.9088584050220879|0.3851747567456406                           |0.3236438845352696 |3.887026887198571    |0.0 |0.0  |0.1681516475|0.35      |0.5051546  |1.5               |10.0     |
|like_per_post|25806.0                      |0.9758583275207316|3.6355852761402                              |5.778244836801792  |7.536645629483825    |0.0 |0.0  |0.97515245  |2.0       |4.0666666  |26.8              |170.78572|
|post_per_message|25806.0                      |0.965821901883283|3.4220980107529333                           |12.386167727775671 |15.90018746496957    |0.0 |0.0  |0.21370469  |0.7222222 |2.4210527  |46.5              |512.0    |
|unfriend_per_newfriend|25806.0                      |0.23510036425637448|0.08656659140110828                          |0.24431719258071752|4.654930976207499    |0.0 |0.0  |0.0         |0.0       |0.0        |1.0               |4.0      |
|dislike_pcnt|25806.0                      |0.9486166007905138|0.23051088514168408                          |0.20743508629090027|1.248231134052179    |0.0 |0.0  |0.071428575 |0.16666667|0.33333334 |0.8888889         |1.0      |
|unfriend_per_newfriend_scaled|25806.0                      |0.45481670929241264|0.08890653558360459                          |0.19417880433632187|5.067467497828502    |0.0 |0.0  |0.0         |0.0       |0.0952381  |1.037037          |4.2      |
|newfriend_pcnt_chng|25806.0                      |0.6977834612105712|0.18253982911247382                          |0.9196034171977002 |2.950901871000234    |-1.0|-1.0 |-0.25       |0.0       |0.33333337 |4.0               |10.0     |
|days_since_newfriend|25806.0                      |0.7712159962799349|7.450709137409905                            |11.607070121598447 |3.0593325319924807   |0.0 |0.0  |1.0         |3.0       |9.0        |57.0              |116.0    |
|unfriend_28day_avg_84day_obs|25806.0                      |0.5039525691699605|0.24212716073781285                          |0.2939168878211054 |1.282504509515786    |0.0 |0.0  |0.0         |0.33333334|0.33333334 |1.0               |2.3333333|
|unfriend_28day_avg_84day_obs_scaled|25806.0                      |0.5039525691699605|0.30910598619545837                          |0.39562381762618437|1.715533274119719    |0.0 |0.0  |0.0         |0.33333334|0.5283019  |1.5555556         |4.2      |

## Scoring metrics
                                                     
The metrics are transformed based on the skew and whether they are negative:
fattail_score are negative and highly skewed.
and skew scores are positive but highly skewed.

|FIELD1|skew_score                   |fattail_score|mean                                         |std                |
|------|-----------------------------|-------------|---------------------------------------------|-------------------|
|like_per_month|True                         |False        |3.696694558351651                            |1.3064737670738882 |
|newfriend_per_month|False                        |False        |6.624002170037976                            |7.993498358467066  |
|post_per_month|True                         |False        |3.0016729786334104                           |1.1735840347725328 |
|adview_per_month|True                         |False        |2.9827594958447414                           |1.208859661500904  |
|dislike_per_month|True                         |False        |2.2392088105792336                           |1.061185533167938  |
|unfriend_per_month|False                        |False        |0.3027202976052081                           |0.54855852163725   |
|message_per_month|True                         |False        |3.2330272598368857                           |1.3274682151528998 |
|reply_per_month|True                         |False        |2.2352085552908236                           |1.3292585899054798 |
|account_tenure|False                        |False        |71.06510113926994                            |26.747373644961094 |
|adview_per_post|True                         |False        |0.7761967189806431                           |0.5474739107542783 |
|reply_per_message|False                        |False        |0.3851747567456406                           |0.3236438845352696 |
|like_per_post|True                         |False        |1.2087999061324468                           |0.7251477440695786 |
|post_per_message|True                         |False        |0.8453150738349696                           |0.8771211356211015 |
|unfriend_per_newfriend|False                        |False        |0.08656659140110828                          |0.24431719258071752|
|dislike_pcnt|False                        |False        |0.23051088514168408                          |0.20743508629090027|
|unfriend_per_newfriend_scaled|True                         |False        |0.07400563772805094                          |0.13836114274615283|
|newfriend_pcnt_chng|False                        |False        |0.18253982911247382                          |0.9196034171977002 |
|days_since_newfriend|False                        |False        |7.450709137409905                            |11.607070121598447 |
|unfriend_28day_avg_84day_obs|False                        |False        |0.24212716073781285                          |0.2939168878211054 |
|unfriend_28day_avg_84day_obs_scaled|False                        |False        |0.30910598619545837                          |0.39562381762618437|
                                                     

## Hierarchichal Clustering
                                                     
After dataset generation, the metrics are scaled and grouped together into groups based in correlation between metrics.
These are the groupings of metrics based on hierarchical clustering.
                                                     

|FIELD1|metrics                      |
|------|-----------------------------|
|metric_group_0|adview_per_month&#124;adview_per_post&#124;like_per_month&#124;like_per_post&#124;newfriend_per_month&#124;post_per_message&#124;post_per_month|
|metric_group_1|unfriend_28day_avg_84day_obs&#124;unfriend_28day_avg_84day_obs_scaled&#124;unfriend_per_month&#124;unfriend_per_newfriend&#124;unfriend_per_newfriend_scaled|
|metric_group_2|message_per_month&#124;reply_per_month|
|dislike_per_month|dislike_per_month            |
|account_tenure|account_tenure               |
|reply_per_message|reply_per_message            |
|dislike_pcnt|dislike_pcnt                 |
|newfriend_pcnt_chng|newfriend_pcnt_chng          |
|days_since_newfriend|days_since_newfriend         |
                                                     
This is the pipeline for dataset grouping and scoring:

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



