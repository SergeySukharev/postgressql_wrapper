# -------------------------------
# ---- 2.2.11 Итог. Базовый. ----
# -------------------------------


# -- Сверка кол-ва записей 
query_2_2_11_1 = ("""select 	count(0)
from (
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
	and group_type in ('базовый')
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
where b.value is null
union all
select 	count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	clc.ss in ('ARM', 'SAS', 'NSAS')
	and metric_type_id in (12,2,18)
	and val_type_id = 7
	and date_type_id = 3
	and group_type in ('базовый')
	and clc.calc_rule = 'growplan'
	and clc.%s""")


# -- Сравнение всех записей в таблицах
query_2_2_11_2 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, 
		a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
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
	and group_type in ('базовый')
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
where b.value is null
except 
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	clc.ss in ('ARM', 'SAS', 'NSAS')
	and metric_type_id in (12,2,18)
	and val_type_id = 7
	and date_type_id = 3
	and group_type in ('базовый')
	and clc.calc_rule = 'growplan'
	and clc.%s""")



# -------------------------------
# ---- Итог. Среднесуточный. ----
# -------------------------------


# -- Сверка кол-ва записей 
query_2_2_11_3 = ("""select 	count(0)
from (
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t ind 
	join dm_stg.d_date_t dte
		on	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on ind.hcode_id = hcd.id
where metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and group_type in ('среднесуточный')
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
union all 
select 	count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	clc.ss in ('ARM', 'SAS', 'NSAS')
	and metric_type_id in (12,2,18)
	and val_type_id = 7
	and date_type_id = 3
	and group_type in ('среднесуточный')
	and clc.calc_rule = 'growplan'
	and clc.%s""")


# -- Сравнение всех записей в таблицах
query_2_2_11_4 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, 
		a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t ind 
	join dm_stg.d_date_t dte
		on	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on ind.hcode_id = hcd.id
where metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and group_type in ('среднесуточный')
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
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null
except 
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	clc.ss in ('ARM', 'SAS', 'NSAS')
	and metric_type_id in (12,2,18)
	and val_type_id = 7
	and date_type_id = 3
	and group_type in ('среднесуточный')
	and clc.calc_rule = 'growplan'
	and clc.%s""")


QUERYS_2_11 = [v for v in locals() if v.startswith('query')]


QUERYS_2_11_EQUAL = [n for n in QUERYS_2_11 if QUERYS_2_11.index(n) % 2 == 0]
QUERYS_2_11_EMPTY = [n for n in QUERYS_2_11 if QUERYS_2_11.index(n) % 2 != 0]