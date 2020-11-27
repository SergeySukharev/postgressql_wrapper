# ------------------------------------------
# ---- Общая сверка dm_stg.calc_grow_t. ----
# ------------------------------------------


query_2_2_13_1 = ("""-- Нарастающие итоги для плана + показатели без суток сверка кол-ва
select 'tgt', count(0) from dm_rep.dm_all_indicators_v ind
where calc_rule = 'growplan'
    and %s
union all
select 'src', count(0) from(
-- Нарастающий итог по суткам с начала месяца	
select 0 from (
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 3 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and group_type in ('базовый', 'среднесуточный')
    and dte.%s) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
	and val_type_id = 3
	and date_type_id = 3
	and group_type in ('базовый', 'среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
union all
-- Нарастающий итог по суткам с начала квартала
select 0 from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
			unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type in ('базовый', 'среднесуточный')
    and dte.%s) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
	and val_type_id = 8
	and date_type_id = 3
	and group_type in ('базовый', 'среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
union all
-- Нарастающий итог по суткам с начала года
select 0 from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type in ('базовый', 'среднесуточный')
    and dte.%s) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
	and val_type_id = 1
	and date_type_id = 3
	and group_type in ('базовый', 'среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
union all
-- Нарастающий итог по месяцам с начала квартала
select 0 from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 9 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type in ('базовый', 'среднесуточный')
    and dte.%s) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
	and val_type_id = 9
	and date_type_id = 4
	and group_type in ('базовый', 'среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
union all
-- Нарастающий итог по месяцам с начала года
select 0 from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 
			5 as val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind 
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where 	metric_type_id in (12,2,18)
		and ind.val_type_id = 7
		and ind.date_type_id = 4
		and hcd.group_type in ('базовый', 'среднесуточный')
        and ind.%s
	union all 
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 
			5 as val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind 
	where 	metric_type_id in (12,2,18)
		and ind.val_type_id = 7
		and ind.date_type_id = 4
		and hcode_id = '00025'
        and ind.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where 	hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
		and val_type_id = 5
		and date_type_id = 4
		and (group_type in ('базовый', 'среднесуточный') or hcode_id = '00025')) b
	on  	a.hcode_id = b.hcode_id
		and a.org_id = b.org_id 
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
		and a.unit_id = b.unit_id
where b.value is null
union all
-- Итог
select 0 from (
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dte.dt, value/dte.month_length as value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t ind 
	join dm_stg.d_date_t dte
		on	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on ind.hcode_id = hcd.id
where metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and group_type in ('базовый', 'среднесуточный')
    and dte.%s
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and metric_type_id in (12,2,18)
	and val_type_id = 7
	and date_type_id = 3
	and group_type in ('базовый', 'среднесуточный')) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
) sum""")

QUERYS_2_13 = [v for v in locals() if v.startswith('query')]


# /*
#  * Для дебага

# -----------------------------------------------------
# ---- Нарастающий итог по суткам с начала месяца. ----
# -----------------------------------------------------

# select 'tgt', count(0) from dm_rep.dm_all_indicators_v
# where 	val_type_id = 3
# 	and date_type_id = 3
# 	and calc_rule = 'growplan'
# union all
# select 'src', count(0)	from (
# select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 3 as val_type_id, 
# 		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 	from dm_stg.calc_src_indicators_t ind 
# 	join dm_stg.d_date_t dte
# 		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
# 		and date_part('year', ind.dt) = date_part('year', dte.dt)
# 	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 		on ind.hcode_id = hcd.id
# where 	metric_type_id in (12,2,18)
# 	and ind.val_type_id = 7
# 	and ind.date_type_id = 4
# 	and group_type in ('базовый', 'среднесуточный')) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 	and val_type_id = 3
# 	and date_type_id = 3
# 	and group_type in ('базовый', 'среднесуточный')) b
# on  	a.hcode_id = b.hcode_id
# 	and a.org_id = b.org_id
# 	and a.duch_id = b.duch_id
# 	and a.nod_id = b.nod_id 
# 	and a.date_type_id = b.date_type_id
# 	and a.metric_type_id = b.metric_type_id
# 	and a.cargo_type_id = b.cargo_type_id
# 	and a.val_type_id = b.val_type_id 
# 	and a.dt = b.dt
# 	and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 	and a.unit_id = b.unit_id
# where b.value is null


# # -------------------------------------------------------
# # ---- Нарастающий итог по суткам с начала квартала. ----
# # -------------------------------------------------------

# select 'tgt', count(0) from dm_rep.dm_all_indicators_v
# where 	val_type_id = 8
# 	and date_type_id = 3
# 	and calc_rule = 'growplan'
# union all
# select 'src', count(0) from (
# 	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
# 			unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 		from dm_stg.calc_src_indicators_t ind 
# 		join dm_stg.d_date_t dte
# 			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
# 			and date_part('year', ind.dt) = date_part('year', dte.dt)
# 		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# where 	metric_type_id in (12,2,18)
# 	and ind.val_type_id = 7
# 	and ind.date_type_id = 4
# 	and hcd.group_type in ('базовый', 'среднесуточный')) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 	and val_type_id = 8
# 	and date_type_id = 3
# 	and group_type in ('базовый', 'среднесуточный')) b
# on  	a.hcode_id = b.hcode_id
# 	and a.org_id = b.org_id
# 	and a.duch_id = b.duch_id
# 	and a.nod_id = b.nod_id 
# 	and a.date_type_id = b.date_type_id
# 	and a.metric_type_id = b.metric_type_id
# 	and a.cargo_type_id = b.cargo_type_id
# 	and a.val_type_id = b.val_type_id 
# 	and a.dt = b.dt
# 	and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 	and a.unit_id = b.unit_id
# where b.value is null



# # --------------------------------------------------------
# # ---- Нарастающий итог по месяцам с начала квартала. ----
# # --------------------------------------------------------
	
# select 'tgt', count(0) from dm_rep.dm_all_indicators_v
# where  	val_type_id = 9
# 	and date_type_id = 4
# 	and calc_rule = 'growplan'
# union all
# select 'src', count(0)	from (
# 	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 9 as val_type_id, 
# 		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 		from dm_stg.calc_src_indicators_t ind 
# 		join dm_stg.d_date_t dte
# 			on dte.dt = ind.dt
# 		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# where 	metric_type_id in (12,2,18)
# 	and ind.val_type_id = 7
# 	and ind.date_type_id = 4
# 	and hcd.group_type in ('базовый', 'среднесуточный')) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 	and val_type_id = 9
# 	and date_type_id = 4
# 	and group_type in ('базовый', 'среднесуточный')) b
# on  	a.hcode_id = b.hcode_id
# 	and a.org_id = b.org_id
# 	and a.duch_id = b.duch_id
# 	and a.nod_id = b.nod_id 
# 	and a.date_type_id = b.date_type_id
# 	and a.metric_type_id = b.metric_type_id
# 	and a.cargo_type_id = b.cargo_type_id
# 	and a.val_type_id = b.val_type_id 
# 	and a.dt = b.dt
# 	and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 	and a.unit_id = b.unit_id
# where b.value is null


# # ---------------------------------------------------
# # ---- Нарастающий итог по суткам с начала года. ----
# # ---------------------------------------------------
	
# select 'tgt', count(0) from dm_rep.dm_all_indicators_v
# where 	val_type_id = 1
# 	and date_type_id = 3
# 	and calc_rule = 'growplan'
# union all
# select 'src', count(0) from (
# 	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 1 as val_type_id, 
# 		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 		from dm_stg.calc_src_indicators_t ind
# 		join dm_stg.d_date_t dte
# 			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
# 			and date_part('year', ind.dt) = date_part('year', dte.dt)
# 		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# where 	metric_type_id in (12,2,18)
# 	and ind.val_type_id = 7
# 	and ind.date_type_id = 4
# 	and hcd.group_type in ('базовый', 'среднесуточный')) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 	and val_type_id = 1
# 	and date_type_id = 3
# 	and group_type in ('базовый', 'среднесуточный')) b
# on  	a.hcode_id = b.hcode_id
# 	and a.org_id = b.org_id
# 	and a.duch_id = b.duch_id
# 	and a.nod_id = b.nod_id 
# 	and a.date_type_id = b.date_type_id
# 	and a.metric_type_id = b.metric_type_id
# 	and a.cargo_type_id = b.cargo_type_id
# 	and a.val_type_id = b.val_type_id 
# 	and a.dt = b.dt
# 	and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 	and a.unit_id = b.unit_id
# where b.value is null

	
# # ----------------------------------------------------
# # ---- Нарастающий итог по месяцам с начала года. ----
# # ----------------------------------------------------
	
# select 'tgt', count(0) from dm_rep.dm_all_indicators_v
# where 	val_type_id = 5
# 	and date_type_id = 4
# 	and calc_rule = 'growplan'
# union all
# select 'src', count(0)	from (
# 	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 
# 			5 as val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where 	metric_type_id in (12,2,18)
# 		and ind.val_type_id = 7
# 		and ind.date_type_id = 4
# 		and hcd.group_type in ('базовый', 'среднесуточный')
# 	union all 
# 	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 
# 			5 as val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 		from dm_stg.calc_src_indicators_t ind 
# 	where 	metric_type_id in (12,2,18)
# 		and ind.val_type_id = 7
# 		and ind.date_type_id = 4
# 		and hcode_id = '00025'
# 	) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where 	hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 		and val_type_id = 5
# 		and date_type_id = 4
# 		and (group_type in ('базовый', 'среднесуточный') or hcode_id = '00025')) b
# 	on  	a.hcode_id = b.hcode_id
# 		and a.org_id = b.org_id 
# 		and a.duch_id = b.duch_id
# 		and a.nod_id = b.nod_id 
# 		and a.date_type_id = b.date_type_id
# 		and a.metric_type_id = b.metric_type_id
# 		and a.cargo_type_id = b.cargo_type_id
# 		and a.val_type_id = b.val_type_id 
# 		and a.dt = b.dt
# 		and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 		and a.unit_id = b.unit_id
# where b.value is null

	
# # ---------------
# # ---- Итог. ----
# # ---------------
	
# select 	count(0) from dm_rep.dm_all_indicators_v
# where 	val_type_id = 7
# 	and date_type_id = 3
# 	and calc_rule = 'growplan'
# union all
# select 	count(0) from (
# select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, val_type_id, 
# 		unit_id, dte.dt, value/dte.month_length as value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
# 	from dm_stg.calc_src_indicators_t ind 
# 	join dm_stg.d_date_t dte
# 		on	date_part('month', ind.dt) = date_part('month', dte.dt)
# 		and date_part('year', ind.dt) = date_part('year', dte.dt)
# 	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 		on ind.hcode_id = hcd.id
# where metric_type_id in (12,2,18)
# 	and ind.val_type_id = 7
# 	and ind.date_type_id = 4
# 	and group_type in ('базовый', 'среднесуточный')
# 	) a
# left join ( -- Секция выявления более приоритетных дублей
# 	select  *
# 		from dm_stg.calc_src_indicators_t ind 
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
# 		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
# 		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
# 			on ind.hcode_id = hcd.id
# 	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
# 	and metric_type_id in (12,2,18)
# 	and val_type_id = 7
# 	and date_type_id = 3
# 	and group_type in ('базовый', 'среднесуточный')) b
# on  	a.hcode_id = b.hcode_id
# 	and a.org_id = b.org_id
# 	and a.duch_id = b.duch_id
# 	and a.nod_id = b.nod_id 
# 	and a.date_type_id = b.date_type_id
# 	and a.metric_type_id = b.metric_type_id
# 	and a.cargo_type_id = b.cargo_type_id
# 	and a.val_type_id = b.val_type_id 
# 	and a.dt = b.dt
# 	and a.dir_id = b.dir_id 
# and a.depo_id = b.depo_id 
# and a.dep_id = b.dep_id
# and a.kato_id = b.kato_id
# and a.vids_id = b.vids_id
# 	and a.unit_id = b.unit_id
# where b.value is null

# */