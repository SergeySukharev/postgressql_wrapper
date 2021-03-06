# ----------------------------------------------------------------
# ---- Нарастающий итог по суткам с начала квартала. Базовый. ----
# ----------------------------------------------------------------


# /*
# sum(CQ where val_type=7 and date_type=4) + (dt=01.CM.CY and val_type=7 and date_type=4/month_length(CM)*количество прошедших дней)	
# Если нет строчки 8 12/2 3 (целевые значения), берем значения за прошедшие месяцы до "текущего", прибавляем нарастающий итог по суткам с начала месяца
#  */
 

# -- Первый месяц квартала --

# -- Сверка кол-ва записей 
query_2_2_3_1 = ("""select 'tgt', count(0) from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 8
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 1
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_rep.dm_all_indicators_v ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 1
	and dte.%s
	) a
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
	and group_type in ('базовый')) b
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")


# Сравнение всех записей в таблицах
query_2_2_3_2 = ("""select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, 
		clc.metric_type_id, clc.cargo_type_id, clc.val_type_id, clc.unit_id, clc.dt, clc.value as value, 
		clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join dm_stg.d_date_t dte
		on dte.dt = clc.dt
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd 
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and val_type_id = 8
	and date_type_id = 3
	and dte.month_from_quater = 1
	and hcd.group_type = 'базовый'
	and clc.%s
except
select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
	select ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, 
		ind.metric_type_id, ind.cargo_type_id, 8 as val_type_id, ind.unit_id, dte.dt, ind.value/dte.month_length*dte.day_of_month as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_rep.dm_all_indicators_v 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18)
	 ) ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
			and dte.month_from_quater = 1
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on 	ind.hcode_id = hcd.id
			and hcd.group_type = 'базовый'
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
	and val_type_id = 8
	and date_type_id = 3
	and group_type in ('базовый')) b
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null	""")



# -- Второй месяц квартала --
# ---------------------------

# -- Сверка кол-ва записей 
query_2_2_3_3 = ("""select 'tgt', count(0) from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 8
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 2
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_rep.dm_all_indicators_v ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 2
	and dte.%s
	) a
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
	and group_type in ('базовый')) b
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")



# -- Третий месяц квартала --
# ---------------------------

# -- Сверка кол-ва записей 
query_2_2_3_6 = ("""select 'tgt', count(0) from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 8
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 3
	and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_rep.dm_all_indicators_v ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where 	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type = 'базовый'
	and dte.month_from_quater = 3
	and dte.%s
	) a
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
	and group_type in ('базовый')) b
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")


QUERYS_2_3_EQUAL = ['query_2_2_3_1', 'query_2_2_3_3', 'query_2_2_3_6']

QUERYS_2_3_EMPTY = ['query_2_2_3_2']