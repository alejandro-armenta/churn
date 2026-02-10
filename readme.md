# Churn Forecasting

I worked in customer retention making churn prediction for customers.

This is the pipeline for dataset generation:

![ale]('Cohorts/Screenshot 2026-01-18 225012.png')

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

