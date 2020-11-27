# ------------------------------------------------------------------------
# ---- 2.1.6 Нарастающий итог по суткам с начала года. Среднесуточный ----
# ------------------------------------------------------------------------

# --------------------------
# Первый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_1 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 1
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
		unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 1
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_1_6_2 = ("""select 	clc.hcode_id, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.ss, clc.value::numeric(16,8), clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 1
	and clc.%s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.ss, a.value::numeric(16,8), a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, ind.value as value, ind.ss, 
		ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 1
	 ) as ind 
	join dm_stg.d_date_t dte
		on dte.dt = ind.dt	
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type = 'среднесуточный') b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# --------------------------
# Второй месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_3 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 2
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 2
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_1_6_4 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length))::numeric(20,12) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	(select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 2
		 	) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
			where ind.%s
			) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,12), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 2
	and clc.%s""")

# --------------------------
# Третий месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_5 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 3
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id	
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 3
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_1_6_6 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt,
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length 
		+ ind3.value*dte3.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	(	select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 3
	 		) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
			where ind.%s
			) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 3
	and clc.%s""")

# --------------------------
# Четвертый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_7 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 4
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 4
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_8 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value::numeric(25,6), a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length 
		+ ind3.value*dte3.month_length + ind4.value*dte4.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length)) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	( 	select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 4
			) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
			where ind.%s
			) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 4
	and clc.%s""")

# --------------------------
# Пятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_9 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 5
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 5
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_10 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt,
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 5
	 ) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 5
	and clc.%s""")

# --------------------------
# Шестой месяц года
# --------------------------


query_2_1_6_11 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 6
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id	
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 6
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")


# Сверка кол-ва записей
query_2_1_6_12 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt,
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	( 	select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 6
	 		) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 6
	and clc.%s""")

# --------------------------
# Седьмой месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_13 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 7
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id	
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 7
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_14 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length))::numeric(20,6) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	( 	select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 7
	 		) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 7
	and clc.%s""")

# --------------------------
# Восьмой месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_15 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 8
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 8
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_16 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value::numeric(20,8), a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length + ind8.value*dte8.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length
		+ (case when ind8.value is null then 0 else 1 end)*dte8.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 8
	 ) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join dm_stg.d_date_t dte8 on dte8.dt = (date(ind.dt) - interval '7 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind8.org_id
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
			and ind.dir_id = ind8.dir_id 
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind.vids_id = ind8.vids_id
			and ind.kato_id = ind8.kato_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 8
	and clc.%s""")


# --------------------------
# Девятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_17 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 9
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 9
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_18 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length + ind8.value*dte8.month_length + ind9.value*dte9.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length
		+ (case when ind8.value is null then 0 else 1 end)*dte8.month_length
		+ (case when ind9.value is null then 0 else 1 end)*dte9.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from 	( 	select * from dm_rep.dm_all_indicators_v 
				where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 9
	 		) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join dm_stg.d_date_t dte8 on dte8.dt = (date(ind.dt) - interval '7 month')
	join dm_stg.d_date_t dte9 on dte9.dt = (date(ind.dt) - interval '8 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind8.org_id
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
			and ind.dir_id = ind8.dir_id 
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind.vids_id = ind8.vids_id
			and ind.kato_id = ind8.kato_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind9.org_id
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
			and ind.dir_id = ind9.dir_id 
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind.vids_id = ind9.vids_id
			and ind.kato_id = ind9.kato_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 9
	and clc.%s""")


# --------------------------
# Десятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_19 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 10
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id	
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 10
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_20 = ("""select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 10
	and clc.%s
except
select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length + ind8.value*dte8.month_length + ind9.value*dte9.month_length 
		+ ind10.value*dte10.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length
		+ (case when ind8.value is null then 0 else 1 end)*dte8.month_length
		+ (case when ind9.value is null then 0 else 1 end)*dte9.month_length
		+ (case when ind10.value is null then 0 else 1 end)*dte10.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 10
	 ) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join dm_stg.d_date_t dte8 on dte8.dt = (date(ind.dt) - interval '7 month')
	join dm_stg.d_date_t dte9 on dte9.dt = (date(ind.dt) - interval '8 month')	
	join dm_stg.d_date_t dte10 on dte10.dt = (date(ind.dt) - interval '9 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind8.org_id
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
			and ind.dir_id = ind8.dir_id 
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind.vids_id = ind8.vids_id
			and ind.kato_id = ind8.kato_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind9.org_id
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
			and ind.dir_id = ind9.dir_id 
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind.vids_id = ind9.vids_id
			and ind.kato_id = ind9.kato_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind10.org_id
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
			and ind.dir_id = ind10.dir_id 
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind.vids_id = ind10.vids_id
			and ind.kato_id = ind10.kato_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# --------------------------
# Одиннадцатый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_21 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 11
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 11
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_22 = ("""select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 11
	and clc.%s
except
select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length + ind8.value*dte8.month_length + ind9.value*dte9.month_length 
		+ ind10.value*dte10.month_length + ind11.value*dte11.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length
		+ (case when ind8.value is null then 0 else 1 end)*dte8.month_length
		+ (case when ind9.value is null then 0 else 1 end)*dte9.month_length
		+ (case when ind10.value is null then 0 else 1 end)*dte10.month_length
		+ (case when ind11.value is null then 0 else 1 end)*dte11.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 11
	 ) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join dm_stg.d_date_t dte8 on dte8.dt = (date(ind.dt) - interval '7 month')
	join dm_stg.d_date_t dte9 on dte9.dt = (date(ind.dt) - interval '8 month')	
	join dm_stg.d_date_t dte10 on dte10.dt = (date(ind.dt) - interval '9 month')
	join dm_stg.d_date_t dte11 on dte11.dt = (date(ind.dt) - interval '10 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind8.org_id
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
			and ind.dir_id = ind8.dir_id 
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind.vids_id = ind8.vids_id
			and ind.kato_id = ind8.kato_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind9.org_id
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
			and ind.dir_id = ind9.dir_id 
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind.vids_id = ind9.vids_id
			and ind.kato_id = ind9.kato_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind10.org_id
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
			and ind.dir_id = ind10.dir_id 
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind11
		on (ind.hcode_id = ind11.hcode_id
			and ind.org_id = ind11.org_id
			and ind.metric_type_id = ind11.metric_type_id
			and ind.cargo_type_id = ind11.cargo_type_id
			and ind.unit_id = ind11.unit_id
			and ind.duch_id = ind11.duch_id
			and ind.nod_id = ind11.nod_id
			and ind.dir_id = ind11.dir_id 
and ind.depo_id = ind11.depo_id
and ind.dep_id = ind11.dep_id
			and ind.vids_id = ind11.vids_id
			and ind.kato_id = ind11.kato_id
			and ind11.val_type_id = 7
			and ind11.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind11.dt)+10)
			and date_part('year', ind.dt) = date_part('year', ind11.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

# --------------------------
# Двенадцатый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_1_6_23 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'grow'
	and val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', dt) = 12
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id	
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (1,17)
	and ind.val_type_id = 3
	and ind.date_type_id = 3
	and hcd.group_type = 'среднесуточный'
	and date_part('month', ind.dt) = 12
	and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")

query_2_1_6_24 = ("""select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.kato_id, clc.vids_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc 
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'grow'
	and  hcd.group_type = 'среднесуточный'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 12
	and clc.%s
except
select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, 
		((ind.value*dte.day_of_month + ind2.value*dte2.month_length + ind3.value*dte3.month_length 
		+ ind4.value*dte4.month_length + ind5.value*dte5.month_length + ind6.value*dte6.month_length 
		+ ind7.value*dte7.month_length + ind8.value*dte8.month_length + ind9.value*dte9.month_length 
		+ ind10.value*dte10.month_length + ind11.value*dte11.month_length + ind12.value*dte12.month_length)
		/((case when ind.value is null then 0 else 1 end)*dte.day_of_month 
		+ (case when ind2.value is null then 0 else 1 end)*dte2.month_length
		+ (case when ind3.value is null then 0 else 1 end)*dte3.month_length
		+ (case when ind4.value is null then 0 else 1 end)*dte4.month_length
		+ (case when ind5.value is null then 0 else 1 end)*dte5.month_length
		+ (case when ind6.value is null then 0 else 1 end)*dte6.month_length
		+ (case when ind7.value is null then 0 else 1 end)*dte7.month_length
		+ (case when ind8.value is null then 0 else 1 end)*dte8.month_length
		+ (case when ind9.value is null then 0 else 1 end)*dte9.month_length
		+ (case when ind10.value is null then 0 else 1 end)*dte10.month_length
		+ (case when ind11.value is null then 0 else 1 end)*dte11.month_length
		+ (case when ind12.value is null then 0 else 1 end)*dte12.month_length))::numeric(20,8) as value,
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where vt = 'BASE' and val_type_id = 3 and date_type_id = 3 and metric_type_id in (1,17) and date_part('month', dt) = 12
	 ) as ind 
	join dm_stg.d_date_t dte on dte.dt = date(ind.dt)
	join dm_stg.d_date_t dte2 on dte2.dt = (date(ind.dt) - interval '1 month')
	join dm_stg.d_date_t dte3 on dte3.dt = (date(ind.dt) - interval '2 month')
	join dm_stg.d_date_t dte4 on dte4.dt = (date(ind.dt) - interval '3 month')
	join dm_stg.d_date_t dte5 on dte5.dt = (date(ind.dt) - interval '4 month')
	join dm_stg.d_date_t dte6 on dte6.dt = (date(ind.dt) - interval '5 month')
	join dm_stg.d_date_t dte7 on dte7.dt = (date(ind.dt) - interval '6 month')
	join dm_stg.d_date_t dte8 on dte8.dt = (date(ind.dt) - interval '7 month')
	join dm_stg.d_date_t dte9 on dte9.dt = (date(ind.dt) - interval '8 month')	
	join dm_stg.d_date_t dte10 on dte10.dt = (date(ind.dt) - interval '9 month')
	join dm_stg.d_date_t dte11 on dte11.dt = (date(ind.dt) - interval '10 month')
	join dm_stg.d_date_t dte12 on dte12.dt = (date(ind.dt) - interval '11 month')
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'среднесуточный'
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.vids_id = ind2.vids_id
			and ind.kato_id = ind2.kato_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.vids_id = ind3.vids_id
			and ind.kato_id = ind3.kato_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind4.org_id
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
			and ind.dir_id = ind4.dir_id 
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind.vids_id = ind4.vids_id
			and ind.kato_id = ind4.kato_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind5.org_id
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
			and ind.dir_id = ind5.dir_id 
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind.vids_id = ind5.vids_id
			and ind.kato_id = ind5.kato_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind6.org_id
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
			and ind.dir_id = ind6.dir_id 
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind.vids_id = ind6.vids_id
			and ind.kato_id = ind6.kato_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind7.org_id
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
			and ind.dir_id = ind7.dir_id 
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind.vids_id = ind7.vids_id
			and ind.kato_id = ind7.kato_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind8.org_id
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
			and ind.dir_id = ind8.dir_id 
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind.vids_id = ind8.vids_id
			and ind.kato_id = ind8.kato_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind9.org_id
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
			and ind.dir_id = ind9.dir_id 
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind.vids_id = ind9.vids_id
			and ind.kato_id = ind9.kato_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind10.org_id
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
			and ind.dir_id = ind10.dir_id 
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind.vids_id = ind10.vids_id
			and ind.kato_id = ind10.kato_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind11
		on (ind.hcode_id = ind11.hcode_id
			and ind.org_id = ind11.org_id
			and ind.metric_type_id = ind11.metric_type_id
			and ind.cargo_type_id = ind11.cargo_type_id
			and ind.unit_id = ind11.unit_id
			and ind.duch_id = ind11.duch_id
			and ind.nod_id = ind11.nod_id
			and ind.dir_id = ind11.dir_id 
and ind.depo_id = ind11.depo_id
and ind.dep_id = ind11.dep_id
			and ind.vids_id = ind11.vids_id
			and ind.kato_id = ind11.kato_id
			and ind11.val_type_id = 7
			and ind11.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind11.dt)+10)
			and date_part('year', ind.dt) = date_part('year', ind11.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind12
		on (ind.hcode_id = ind12.hcode_id
			and ind.org_id = ind12.org_id
			and ind.metric_type_id = ind12.metric_type_id
			and ind.cargo_type_id = ind12.cargo_type_id
			and ind.unit_id = ind12.unit_id
			and ind.duch_id = ind12.duch_id
			and ind.nod_id = ind12.nod_id
			and ind.dir_id = ind12.dir_id 
and ind.depo_id = ind12.depo_id
and ind.dep_id = ind12.dep_id
			and ind.vids_id = ind12.vids_id
			and ind.kato_id = ind12.kato_id
			and ind12.val_type_id = 7
			and ind12.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind12.dt)+11)
			and date_part('year', ind.dt) = date_part('year', ind12.dt))
		where ind.%s
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (1,17)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id 
	and a.dor_kod = b.dor_kod
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.vids_id = b.vids_id
	and a.kato_id = b.kato_id
	and a.unit_id = b.unit_id
where b.value is null""")



QUERYS_2_1_6 = [v for v in locals() if v.startswith('query')]

QUERYS_2_1_6_EQUAL = [n for n in QUERYS_2_1_6 if QUERYS_2_1_6.index(n) % 2 == 0]
QUERYS_2_1_6_EMPTY = [n for n in QUERYS_2_1_6 if QUERYS_2_1_6.index(n) % 2 != 0]