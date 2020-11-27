# 2.1.1 Нарастающий итог по суткам с начала квартала. Базовый.



# --------------------------
# Первый месяц квартала
# --------------------------


# Сверка кол-ва записей
query_2_1_1_1 = ("""select 'clc', count(0) from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt	
where hcd.group_type = 'базовый'
and calc_rule = 'grow'
and dte.month_from_quater = 1 -- Первый месяц квартала
and clc.val_type_id = 8 -- Нарастающий итог по суткам с начала квартала
and clc.date_type_id = 3 -- Сутки
and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = ind.hcode_id
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt		
where 	hcd.group_type = 'базовый'
	and ind.metric_type_id in (1,17)
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 1
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
	and val_type_id = 8
	and date_type_id = 3
	and group_type = 'базовый') b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
and a.kato_id = b.kato_id
	and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_1_1_2 = ("""select 	clc.hcode_id, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, clc.unit_id, clc.dt, ss, value, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
	join dm_stg.d_date_t dte
			on dte.dt = clc.dt	
where 	hcd.group_type = 'базовый'
	and calc_rule = 'grow'
	and dte.month_from_quater = 1
	and clc.val_type_id = 8
	and clc.date_type_id = 3
	and clc.%s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.ss, a.value, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, ind.unit_id, ind.dt, ss, 
		value, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = ind.hcode_id
	join dm_stg.d_date_t dte
		on dte.dt = ind.dt		
where 	hcd.group_type = 'базовый'
	and ind.metric_type_id in (1,17)
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 1
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
	and val_type_id = 8
	and date_type_id = 3
	and group_type = 'базовый') b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
and a.kato_id = b.kato_id
	and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")

# --------------------------
# Второй месяц квартала
# --------------------------

# Сверка кол-ва записей
query_2_1_1_3 = ("""select 'clc', count(0) from dm_rep.dm_all_indicators_v clc
			join (select distinct id, group_type from dm_stg.d_hcode_t) hcd 	
				on hcd.id = clc.hcode_id
			join dm_stg.d_date_t dte
				on dte.dt = clc.dt	
	where 	hcd.group_type = 'базовый'
		and calc_rule = 'grow'
		and dte.month_from_quater = 2 -- Второй месяц квартала
		and clc.val_type_id = 8 -- Нарастающий итог по суткам с начала квартала
		and clc.date_type_id = 3
		and clc.%s
	union all
	select 'src', count(0) from (
		select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
			unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
			from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
			join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
				on hcd.id = ind.hcode_id
			join dm_stg.d_date_t dte
			on dte.dt = ind.dt		
where 	hcd.group_type = 'базовый'
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 2 -- Второй месяц квартала
	and ind.metric_type_id in (1,17)
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
	and val_type_id = 8
	and date_type_id = 3
	and group_type = 'базовый') b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
and a.kato_id = b.kato_id
	and a.vids_id = b.vids_id
	and a.unit_id = b.unit_id
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_1_1_4 = ("""select 	clc.hcode_id, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, clc.unit_id, 
		clc.dt, ss, value, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
	join dm_stg.d_date_t dte
		on dte.dt = clc.dt	
where 	hcd.group_type = 'базовый'
	and calc_rule = 'grow'
	and dte.month_from_quater = 2 -- Второй месяц квартала
	and clc.val_type_id = 8 -- Нарастающий итог по суткам с начала квартала
	and clc.date_type_id = 3 -- Сутки
	and clc.%s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.ss, a.value, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 8 as val_type_id, ind.unit_id, 
		ind.dt, ind.ss, (ind.value + ind2.value) as value, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 -- Для итога за пред. месяц
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.kato_id = ind2.kato_id
			and ind.vids_id = ind2.vids_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = ind.hcode_id
	join dm_stg.d_date_t dte
		on dte.dt = ind.dt		
where	hcd.group_type = 'базовый'
	and ind.metric_type_id in (1,17)
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 2
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

# --------------------------
# Третий месяц квартала
# --------------------------

# Сверка кол-ва записей
query_2_1_1_5 = ("""select 'clc', count(0) from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt	
where hcd.group_type = 'базовый'
and calc_rule = 'grow'
and dte.month_from_quater = 3 -- Третий месяц квартала
and clc.val_type_id = 8 -- Нарастающий итог по суткам с начала квартала
and clc.date_type_id = 3 -- Сутки
and clc.%s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, ind.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = ind.hcode_id
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt		
where 	hcd.group_type = 'базовый'
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 3 -- Третий месяц квартала
	and ind.metric_type_id in (1,17)
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
query_2_1_1_6 = ("""select  clc.hcode_id, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, clc.unit_id, 
		clc.dt, ss, value, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v clc
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
	join dm_stg.d_date_t dte
		on dte.dt = clc.dt	
where 	hcd.group_type = 'базовый'
	and calc_rule = 'grow'
	and dte.month_from_quater = 3 -- Третий месяц квартала
	and clc.val_type_id = 8 -- Нарастающий итог по суткам с начала квартала
	and clc.date_type_id = 3 -- Сутки
	and clc.%s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.ss, a.value, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, ind.cargo_type_id, 8 as val_type_id, 
		ind.unit_id, ind.dt, ind.ss, (ind.value + ind2.value + ind3.value) as value, 
		ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind2 
		on (ind.hcode_id = ind2.hcode_id
			and ind.org_id = ind2.org_id
			and ind.cargo_type_id = ind2.cargo_type_id
			and ind.unit_id = ind2.unit_id
			and ind.metric_type_id = ind2.metric_type_id
			and ind.duch_id = ind2.duch_id
			and ind.nod_id = ind2.nod_id
			and ind.dir_id = ind2.dir_id 
and ind.depo_id = ind2.depo_id
and ind.dep_id = ind2.dep_id
			and ind.kato_id = ind2.kato_id
			and ind.vids_id = ind2.vids_id
			and ind2.val_type_id = 7
			and ind2.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
			and date_part('year', ind.dt) = date_part('year', ind2.dt))
	left join (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') ind3 
		on (ind.hcode_id = ind3.hcode_id
			and ind.org_id = ind3.org_id
			and ind.cargo_type_id = ind3.cargo_type_id
			and ind.unit_id = ind3.unit_id
			and ind.metric_type_id = ind3.metric_type_id
			and ind.duch_id = ind3.duch_id
			and ind.nod_id = ind3.nod_id
			and ind.dir_id = ind3.dir_id 
and ind.depo_id = ind3.depo_id
and ind.dep_id = ind3.dep_id
			and ind.kato_id = ind3.kato_id
			and ind.vids_id = ind3.vids_id
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = ind.hcode_id
	join dm_stg.d_date_t dte
		on dte.dt = ind.dt		
where 	ind.metric_type_id in (1,17)
	and hcd.group_type = 'базовый'
	and ind.val_type_id = 3 -- Нарастающий итог по суткам с начала месяца
	and ind.date_type_id = 3 -- Сутки
	and dte.month_from_quater = 3
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
	and val_type_id = 8
	and date_type_id = 3
	and group_type = 'базовый') b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id 
	and a.date_type_id = b.date_type_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.val_type_id = b.val_type_id 
	and a.unit_id = b.unit_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id 
and a.depo_id = b.depo_id 
and a.dep_id = b.dep_id
	and a.kato_id = b.kato_id
	and a.vids_id = b.vids_id
where b.value is null""")


QUERYS_2_1_1 = [v for v in locals() if v.startswith('query')]

QUERYS_2_1_1_EQUAL = [n for n in QUERYS_2_1_1 if QUERYS_2_1_1.index(n) % 2 == 0]
QUERYS_2_1_1_EMPTY = [n for n in QUERYS_2_1_1 if QUERYS_2_1_1.index(n) % 2 != 0]