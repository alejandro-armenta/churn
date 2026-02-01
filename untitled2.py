set search_path = 'socialnet7'; 


INSERT into metric_name values (28,concat('unfriend_per_newfriend_scaled'))
ON CONFLICT DO NOTHING;

with num_metric as (
	select account_id, metric_time, metric_value as num_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'unfriend_28avg_84obs_scaled'
	and metric_time between '2020-03-01' and '2020-05-10'
), den_metric as (
	select account_id, metric_time, metric_value as den_value
	from metric m inner join metric_name n on n.metric_name_id=m.metric_name_id
	and n.metric_name = 'newfriend_per_month'
	and metric_time between '2020-03-01' and '2020-05-10'
)
insert into metric (account_id,metric_time,metric_name_id,metric_value)
select d.account_id, d.metric_time, 28,
	case when den_value > 0
	    then coalesce(num_value,0.0)/den_value
	    else 0
    end as metric_value
from den_metric d  left outer join num_metric n
	on n.account_id=d.account_id
	and n.metric_time=d.metric_time
ON CONFLICT DO NOTHING;

----------
RESULT:
