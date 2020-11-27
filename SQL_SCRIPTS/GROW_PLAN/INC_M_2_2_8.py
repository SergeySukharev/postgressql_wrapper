# ------------------------------------------------------------------------------
# ---- 2.2.8 Нарастающий итог по месяцам с начала квартала. Среднесуточный. ----
# ------------------------------------------------------------------------------

# --------------------------
# Первый месяц квартала
# --------------------------

# Сверка кол-ва записей
query_2_2_8_1 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 9
	and date_type_id = 4
	and hcd.group_type = 'среднесуточный'
	and dte.month_from_quater = 1
	and clc.%s
union all
select 'src', count(0)	from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 4 as date_type_id, metric_type_id, cargo_type_id, 9 as val_type_id, 
		unit_id, dte.dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
		from dm_stg.calc_src_indicators_t ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
where	metric_type_id in (12,2,18)
	and ind.val_type_id = 7
	and ind.date_type_id = 4
	and hcd.group_type = 'среднесуточный'
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
	and val_type_id = 9
	and date_type_id = 4
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
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_2_8_2 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 4 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 9 as val_type_id, ind.unit_id, dte.dt, ind.value::numeric(20,12) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18)
	 ) ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
			and dte.month_from_quater = 1
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on 	ind.hcode_id = hcd.id
			and hcd.group_type = 'среднесуточный'
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
	and val_type_id = 9
	and date_type_id = 4
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
	select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, 
			clc.cargo_type_id, clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,12), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
		from dm_rep.dm_all_indicators_v clc
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'среднесуточный'
	and val_type_id = 9
	and date_type_id = 4
	and dte.month_from_quater = 1
	and clc.%s""")

# --------------------------
# Второй месяц квартала
# --------------------------

# Сверка кол-ва записей
query_2_2_8_3 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 9
	and date_type_id = 4
	and hcd.group_type = 'среднесуточный'
	and dte.month_from_quater = 2
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'среднесуточный'
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
	and val_type_id = 9
	and date_type_id = 4
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
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_2_8_4 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 4 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 9 as val_type_id, ind.unit_id, dte.dt, 
		case 
			when 
				ind.hcode_id between '00045' and '00054' 
			then 
				((ind.value + ind2.value)/
				(case when ind.value is not null then 1 else 0 end + case when ind2.value is not null then 1 else 0 end))
			else 
				((ind.value*dte.month_length + ind2.value*dte2.month_length)/
				((case when ind.value is not null then 1 else 0 end)*dte.month_length 
				+ (case when ind2.value is not null then 1 else 0 end)*dte2.month_length)) end as value,  
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from ( 	select * from dm_stg.calc_src_indicators_t 
			where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18)
		 ) ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
			and dte.month_from_quater = 2
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on 	ind.hcode_id = hcd.id
			and hcd.group_type = 'среднесуточный'
		left join dm_stg.calc_src_indicators_t ind2  -- Для пред. месяца
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
		join dm_stg.d_date_t dte2 on dte2.dt = ind2.dt
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
	and val_type_id = 9
	and date_type_id = 4
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, 
		clc.cargo_type_id, clc.val_type_id, clc.unit_id, clc.dt, clc.value, clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
		from dm_rep.dm_all_indicators_v clc
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'среднесуточный'
	and val_type_id = 9
	and date_type_id = 4
	and dte.month_from_quater = 2
	and clc.%s""")

# --------------------------
# Третий месяц квартала
# --------------------------

# Сверка кол-ва записей
query_2_2_8_5 = ("""select 'tgt', count(0)
		from dm_rep.dm_all_indicators_v clc
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on clc.hcode_id = hcd.id
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
where 	calc_rule = 'growplan'
	and val_type_id = 9
	and date_type_id = 4
	and hcd.group_type = 'среднесуточный'
	and dte.month_from_quater = 3
	and clc.%s
union all
select 'src', count(0)	from (
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
	and hcd.group_type = 'среднесуточный'
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
	and val_type_id = 9
	and date_type_id = 4
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
where b.value is null""")

# Сравнение всех записей в таблицах
query_2_2_8_6 = ("""select 	a.hcode_id, a.hcode_name, a.hcode_unit_name, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 4 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 9 as val_type_id, ind.unit_id, dte.dt, 
		case
			when
				ind.hcode_id between '00045' and '00054' 
			then 
				((ind.value + ind2.value + ind3.value)/
				(case when ind.value is not null then 1 else 0 end + case when ind2.value is not null then 1 else 0 end + 
				case when ind3.value is not null then 1 else 0 end))::numeric(20,10) 
			else
				((ind.value*dte.month_length + ind2.value*dte2.month_length + ind3.value*dte3.month_length)/
				((case when ind.value is not null then 1 else 0 end)*dte.month_length 
				+ (case when ind2.value is not null then 1 else 0 end)*dte2.month_length
				+ (case when ind3.value is not null then 1 else 0 end)*dte3.month_length))::numeric(20,10) 
			end as value, 
		ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
from ( 	select * from dm_stg.calc_src_indicators_t 
		where val_type_id = 7 and date_type_id = 4 and metric_type_id in (12,2,18)
	 ) ind 
		join dm_stg.d_date_t dte
			on dte.dt = ind.dt
			and dte.month_from_quater = 3
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on 	ind.hcode_id = hcd.id
			and hcd.group_type = 'среднесуточный'
		left join dm_stg.calc_src_indicators_t ind2  -- Для пред. месяца
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
		left join dm_stg.calc_src_indicators_t ind3   -- первый месяц квартала
			on (ind.hcode_id = ind3.hcode_id
				and ind.org_id = ind3.org_id
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
		join dm_stg.d_date_t dte2 on dte2.dt = ind2.dt
		join dm_stg.d_date_t dte3 on dte3.dt = ind3.dt
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
	and val_type_id = 9
	and date_type_id = 4
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
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt::date, clc.value::numeric(20,10), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
		from dm_rep.dm_all_indicators_v clc
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'среднесуточный'
	and val_type_id = 9
	and date_type_id = 4
	and dte.month_from_quater = 3
	and clc.%s""")


QUERYS_2_8 = [v for v in locals() if v.startswith('query')]

QUERYS_2_8_EQUAL = [n for n in QUERYS_2_8 if QUERYS_2_8.index(n) % 2 == 0]
QUERYS_2_8_EMPTY = [n for n in QUERYS_2_8 if QUERYS_2_8.index(n) % 2 != 0]
