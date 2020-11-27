# ------------------------------------------------------------------
# ---- 2.2.5 Нарастающий итог по суткам с начала года. Базовый. ----
# ------------------------------------------------------------------

# /*
# sum(CQ where val_type=7 and date_type=4) + (dt=01.CM.CY and val_type=7 and date_type=4/month_length(CM)*количество прошедших дней)	
# Если нет строчки 1 12/2 3 (целевые значения), берем значения за прошедшие месяцы до "текущего", прибавляем нарастающий итог по суткам с начала месяца
#  */
    

# --------------------------
# Первый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_1 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 1
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 1
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
	and val_type_id = 1
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

# Сравнение всех записей в таблицах
query_2_2_5_2 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, ind.value/dte.month_length*dte.day_of_month as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 1
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	where dte.%s
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
	and val_type_id = 1
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value, clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and metric_type_id in (12,2,18)
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 1
	and clc.%s""")

# --------------------------
# Второй месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_3 = ("""select 'tgt', count(0) 
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 2
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 2
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
	and val_type_id = 1
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

# Сравнение всех записей в таблицах
query_2_2_5_4 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, (ind.value/dte.month_length*dte.day_of_month 
		+ ind2.value)::numeric(20,8) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 2
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.dir_id = ind2.dir_id 
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	where dte.%s
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
	and val_type_id = 1
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'базовый'
	and metric_type_id in (12,2,18)
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 2
	and clc.%s""")

# --------------------------
# Третий месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_5 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 3
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 3
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

# Сравнение всех записей в таблицах
query_2_2_5_6 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, (ind.value/dte.month_length*dte.day_of_month 
		+ ind2.value + ind3.value)::numeric(20,6) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 3
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 3
	and clc.%s""")

# --------------------------
# Четвертый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_7 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 4
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 4
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_8 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 1 as val_type_id, ind.unit_id, dte.dt, (ind.value/dte.month_length*dte.day_of_month 
		+ ind2.value + ind3.value + ind4.value)::numeric(20,6) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 4
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
			where dte.%s
			) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and metric_type_id in (12,2,18)
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 4
	and clc.%s""")

# --------------------------
# Пятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_9 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 5
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 5
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_10 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value 
		+ ind5.value)::numeric(20,6) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 5
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 5
	and clc.%s""")

# --------------------------
# Шестой месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_11 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 6
	and clc.%s
union all
select 'src', count(0) from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 6
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_12 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value 
		+ ind5.value + ind6.value)::numeric(20,8) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 6
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 6
	and clc.%s""")

# --------------------------
# Седьмой месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_13 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 7
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 7
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_14 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value 
		+ ind5.value + ind6.value + ind7.value)::numeric(20,6) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 7
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 7
	and clc.%s""")

# --------------------------
# Восьмой месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_15 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 8
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 8
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_16 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value 
		+ ind5.value + ind6.value + ind7.value + ind8.value)::numeric(20,2) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 8
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join dm_stg.calc_src_indicators_t ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind8.dor_kod
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
and ind.kato_id = ind8.kato_id
and ind.vids_id = ind8.vids_id
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,2), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 8
	and clc.%s""")


# --------------------------
# Девятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_17 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 9
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 9
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_18 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value 
		+ ind5.value + ind6.value + ind7.value + ind8.value 
		+ ind9.value)::numeric(20,8) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 9
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join dm_stg.calc_src_indicators_t ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind8.dor_kod
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
and ind.kato_id = ind8.kato_id
and ind.vids_id = ind8.vids_id
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join dm_stg.calc_src_indicators_t ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind9.dor_kod
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
and ind.kato_id = ind9.kato_id
and ind.vids_id = ind9.vids_id
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 9
	and clc.%s""")


# --------------------------
# Десятый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_19 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 10
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 10
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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


query_2_2_5_20 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value + ind5.value + 
		ind6.value + ind7.value + ind8.value + ind9.value + 
		ind10.value)::numeric(20,6) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 10
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join dm_stg.calc_src_indicators_t ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind8.dor_kod
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
and ind.kato_id = ind8.kato_id
and ind.vids_id = ind8.vids_id
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join dm_stg.calc_src_indicators_t ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind9.dor_kod
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
and ind.kato_id = ind9.kato_id
and ind.vids_id = ind9.vids_id
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join dm_stg.calc_src_indicators_t ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind10.dor_kod
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
and ind.kato_id = ind10.kato_id
and ind.vids_id = ind10.vids_id
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 10
	and clc.%s""")

# --------------------------
# Одиннадцатый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_21 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 11
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 11
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_22 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value + ind5.value + 
		ind6.value + ind7.value + ind8.value + ind9.value + 
		ind10.value + ind11.value)::numeric(20,8) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 11
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join dm_stg.calc_src_indicators_t ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind8.dor_kod
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
and ind.kato_id = ind8.kato_id
and ind.vids_id = ind8.vids_id
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join dm_stg.calc_src_indicators_t ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind9.dor_kod
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
and ind.kato_id = ind9.kato_id
and ind.vids_id = ind9.vids_id
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join dm_stg.calc_src_indicators_t ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind10.dor_kod
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
and ind.kato_id = ind10.kato_id
and ind.vids_id = ind10.vids_id
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
	left join dm_stg.calc_src_indicators_t ind11
		on (ind.hcode_id = ind11.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind11.dor_kod
			and ind.metric_type_id = ind11.metric_type_id
			and ind.cargo_type_id = ind11.cargo_type_id
			and ind.unit_id = ind11.unit_id
			and ind.duch_id = ind11.duch_id
			and ind.nod_id = ind11.nod_id
and ind.kato_id = ind11.kato_id
and ind.vids_id = ind11.vids_id
and ind.depo_id = ind11.depo_id
and ind.dep_id = ind11.dep_id
			and ind11.val_type_id = 7
			and ind11.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind11.dt)+10)
			and date_part('year', ind.dt) = date_part('year', ind11.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,8), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 11
	and clc.%s""")

# --------------------------
# Двенадцатый месяц года
# --------------------------

# Сверка кол-ва записей
query_2_2_5_23 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
where 	calc_rule = 'growplan'
	and 	val_type_id = 1
	and date_type_id = 3
	and hcd.group_type = 'базовый'
	and date_part('month', dt) = 12
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'базовый'
	and date_part('month', ind.dt) = 12
	and dte.%s
	) a
left join (-- Секция выявления более приоритетных дублей
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

query_2_2_5_24 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 
		1 as val_type_id, ind.unit_id, dte.dt, 
		(ind.value/dte.month_length*dte.day_of_month + ind2.value + ind3.value + ind4.value + ind5.value + 
		ind6.value + ind7.value + ind8.value + ind9.value + 
		ind10.value + ind11.value + ind12.value)::numeric(20,6) as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18) and date_part('month', dt) = 12
	 ) ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join dm_stg.calc_src_indicators_t ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.dor_kod = ind2.dor_kod
			and ind.metric_type_id = ind2.metric_type_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
and ind.kato_id = ind2.kato_id
and ind.vids_id = ind2.vids_id
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join dm_stg.calc_src_indicators_t ind3
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind3.dor_kod
			and ind.metric_type_id = ind3.metric_type_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
and ind.kato_id = ind3.kato_id
and ind.vids_id = ind3.vids_id
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	left join dm_stg.calc_src_indicators_t ind4
		on (ind.hcode_id = ind4.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind4.dor_kod
			and ind.metric_type_id = ind4.metric_type_id
			and ind.cargo_type_id = ind4.cargo_type_id
			and ind.unit_id = ind4.unit_id
			and ind.duch_id = ind4.duch_id
			and ind.nod_id = ind4.nod_id
and ind.kato_id = ind4.kato_id
and ind.vids_id = ind4.vids_id
and ind.depo_id = ind4.depo_id
and ind.dep_id = ind4.dep_id
			and ind4.val_type_id = 7
			and ind4.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind4.dt)+3)
			and date_part('year', ind.dt) = date_part('year', ind4.dt))
	left join dm_stg.calc_src_indicators_t ind5
		on (ind.hcode_id = ind5.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind5.dor_kod
			and ind.metric_type_id = ind5.metric_type_id
			and ind.cargo_type_id = ind5.cargo_type_id
			and ind.unit_id = ind5.unit_id
			and ind.duch_id = ind5.duch_id
			and ind.nod_id = ind5.nod_id
and ind.kato_id = ind5.kato_id
and ind.vids_id = ind5.vids_id
and ind.depo_id = ind5.depo_id
and ind.dep_id = ind5.dep_id
			and ind5.val_type_id = 7
			and ind5.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind5.dt)+4)
			and date_part('year', ind.dt) = date_part('year', ind5.dt))
	left join dm_stg.calc_src_indicators_t ind6
		on (ind.hcode_id = ind6.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind6.dor_kod
			and ind.metric_type_id = ind6.metric_type_id
			and ind.cargo_type_id = ind6.cargo_type_id
			and ind.unit_id = ind6.unit_id
			and ind.duch_id = ind6.duch_id
			and ind.nod_id = ind6.nod_id
and ind.kato_id = ind6.kato_id
and ind.vids_id = ind6.vids_id
and ind.depo_id = ind6.depo_id
and ind.dep_id = ind6.dep_id
			and ind6.val_type_id = 7
			and ind6.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind6.dt)+5)
			and date_part('year', ind.dt) = date_part('year', ind6.dt))
	left join dm_stg.calc_src_indicators_t ind7
		on (ind.hcode_id = ind7.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind7.dor_kod
			and ind.metric_type_id = ind7.metric_type_id
			and ind.cargo_type_id = ind7.cargo_type_id
			and ind.unit_id = ind7.unit_id
			and ind.duch_id = ind7.duch_id
			and ind.nod_id = ind7.nod_id
and ind.kato_id = ind7.kato_id
and ind.vids_id = ind7.vids_id
and ind.depo_id = ind7.depo_id
and ind.dep_id = ind7.dep_id
			and ind7.val_type_id = 7
			and ind7.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind7.dt)+6)
			and date_part('year', ind.dt) = date_part('year', ind7.dt))
	left join dm_stg.calc_src_indicators_t ind8
		on (ind.hcode_id = ind8.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind8.dor_kod
			and ind.metric_type_id = ind8.metric_type_id
			and ind.cargo_type_id = ind8.cargo_type_id
			and ind.unit_id = ind8.unit_id
			and ind.duch_id = ind8.duch_id
			and ind.nod_id = ind8.nod_id
and ind.kato_id = ind8.kato_id
and ind.vids_id = ind8.vids_id
and ind.depo_id = ind8.depo_id
and ind.dep_id = ind8.dep_id
			and ind8.val_type_id = 7
			and ind8.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind8.dt)+7)
			and date_part('year', ind.dt) = date_part('year', ind8.dt))
	left join dm_stg.calc_src_indicators_t ind9
		on (ind.hcode_id = ind9.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind9.dor_kod
			and ind.metric_type_id = ind9.metric_type_id
			and ind.cargo_type_id = ind9.cargo_type_id
			and ind.unit_id = ind9.unit_id
			and ind.duch_id = ind9.duch_id
			and ind.nod_id = ind9.nod_id
and ind.kato_id = ind9.kato_id
and ind.vids_id = ind9.vids_id
and ind.depo_id = ind9.depo_id
and ind.dep_id = ind9.dep_id
			and ind9.val_type_id = 7
			and ind9.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind9.dt)+8)
			and date_part('year', ind.dt) = date_part('year', ind9.dt))
	left join dm_stg.calc_src_indicators_t ind10
		on (ind.hcode_id = ind10.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind10.dor_kod
			and ind.metric_type_id = ind10.metric_type_id
			and ind.cargo_type_id = ind10.cargo_type_id
			and ind.unit_id = ind10.unit_id
			and ind.duch_id = ind10.duch_id
			and ind.nod_id = ind10.nod_id
and ind.kato_id = ind10.kato_id
and ind.vids_id = ind10.vids_id
and ind.depo_id = ind10.depo_id
and ind.dep_id = ind10.dep_id
			and ind10.val_type_id = 7
			and ind10.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind10.dt)+9)
			and date_part('year', ind.dt) = date_part('year', ind10.dt))
	left join dm_stg.calc_src_indicators_t ind11
		on (ind.hcode_id = ind11.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind11.dor_kod
			and ind.metric_type_id = ind11.metric_type_id
			and ind.cargo_type_id = ind11.cargo_type_id
			and ind.unit_id = ind11.unit_id
			and ind.duch_id = ind11.duch_id
			and ind.nod_id = ind11.nod_id
and ind.kato_id = ind11.kato_id
and ind.vids_id = ind11.vids_id
and ind.depo_id = ind11.depo_id
and ind.dep_id = ind11.dep_id
			and ind11.val_type_id = 7
			and ind11.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind11.dt)+10)
			and date_part('year', ind.dt) = date_part('year', ind11.dt))
	left join dm_stg.calc_src_indicators_t ind12
		on (ind.hcode_id = ind12.hcode_id
			and ind.org_id = ind.org_id
			and ind.dor_kod = ind12.dor_kod
			and ind.metric_type_id = ind12.metric_type_id
			and ind.cargo_type_id = ind12.cargo_type_id
			and ind.unit_id = ind12.unit_id
			and ind.duch_id = ind12.duch_id
			and ind.nod_id = ind12.nod_id
and ind.kato_id = ind12.kato_id
and ind.vids_id = ind12.vids_id
and ind.depo_id = ind12.depo_id
and ind.dep_id = ind12.dep_id
			and ind12.val_type_id = 7
			and ind12.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind12.dt)+11)
			and date_part('year', ind.dt) = date_part('year', ind12.dt))
		where dte.%s
		) a
left join (-- Секция выявления более приоритетных дублей
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and 	hcd.group_type = 'базовый'
	and val_type_id = 1
	and date_type_id = 3
	and date_part('month', dt) = 12
	and clc.%s""")

QUERYS_2_5 = [v for v in locals() if v.startswith('query')]

QUERYS_2_5_EQUAL = [n for n in QUERYS_2_5 if QUERYS_2_5.index(n) % 2 == 0]
QUERYS_2_5_EMPTY = [n for n in QUERYS_2_5 if QUERYS_2_5.index(n) % 2 != 0]