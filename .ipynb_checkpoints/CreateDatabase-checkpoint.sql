set search_path to socialnet7;
    
    with observation_params as (
    select  
        interval '7 day' as metric_period,
        '2020-03-01'::timestamp as obs_start,
        '2020-05-10'::timestamp as obs_end
        )
    select 
        --esta metrica es un churn si o no
        --esta metrica esta dentro del rango de fechas si o no
        
        m.account_id, observation_date, is_churn,
        --sum(case when metric_name_id = 0 then metric_value else 0 end) as like_per_month,
        --sum(case when metric_name_id = 1 then metric_value else 0 end) as newfriend_per_month
    
        SUM(
        CASE
          WHEN metric_name_id = 0 THEN metric_value
          ELSE 0
        END
      ) AS like_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 1 THEN metric_value
          ELSE 0
        END
      ) AS newfriend_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 2 THEN metric_value
          ELSE 0
        END
      ) AS post_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 3 THEN metric_value
          ELSE 0
        END
      ) AS adview_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 4 THEN metric_value
          ELSE 0
        END
      ) AS dislike_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 33 THEN metric_value
          ELSE 0
        END
      ) AS unfriend_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 6 THEN metric_value
          ELSE 0
        END
      ) AS message_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 7 THEN metric_value
          ELSE 0
        END
      ) AS reply_per_month,
      SUM(
        CASE
          WHEN metric_name_id = 21 THEN metric_value
          ELSE 0
        END
      ) AS adview_per_post,
      SUM(
        CASE
          WHEN metric_name_id = 22 THEN metric_value
          ELSE 0
        END
      ) AS reply_per_message,
      SUM(
        CASE
          WHEN metric_name_id = 23 THEN metric_value
          ELSE 0
        END
      ) AS like_per_post,
      SUM(
        CASE
          WHEN metric_name_id = 24 THEN metric_value
          ELSE 0
        END
      ) AS post_per_message,
      SUM(
        CASE
          WHEN metric_name_id = 28 THEN metric_value
          ELSE 0
        END
      ) AS unfriend_per_newfriend,
      SUM(
        CASE
          WHEN metric_name_id = 27 THEN metric_value
          ELSE 0
        END
      ) AS dislike_pcnt,
      SUM(
        CASE
          WHEN metric_name_id = 30 THEN metric_value
          ELSE 0
        END
      ) AS newfriend_pcnt_chng,
      SUM(
        CASE
          WHEN metric_name_id = 31 THEN metric_value
          ELSE 0
        END
      ) AS days_since_newfriend
        
        --observation_date
        --count(m.account_id)
        
        from metric m 
        inner join observation_params on metric_time BETWEEN obs_start and obs_end
        inner join observation o on m.account_id = o.account_id 
        and m.metric_time > (o.observation_date - metric_period)::timestamp 
        and m.metric_time <= o.observation_date::timestamp
    group by m.account_id, m.metric_time, observation_date, is_churn
    order by observation_date, m.account_id