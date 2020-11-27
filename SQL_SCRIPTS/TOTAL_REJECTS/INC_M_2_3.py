# ---------------------------------------------------
# ---- 2.3 Расчет итогов для специфичных показателей ----
# ---------------------------------------------------


# -- Сравнение количества записей
query_2_3_1 = ("""select 'tgt', count(0)
	from dm_rep.dm_all_indicators_v
where	hcode_id in ('00018', '00019', '00020')
	and calc_rule = 'total_rejects'
	and %s
union all
select 'src', count(0) from (
	select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 8 as val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t
where hcode_id in ('00018', '00019', '00020')
and val_type_id = 1
and date_type_id = 3 
and %s)a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and val_type_id = 7
	and date_type_id = 3) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id
	and a.unit_id = b.unit_id
	and a.kato_id = b.kato_id 
	and a.vids_id = b.vids_id
	and a.depo_id = b.depo_id
	and a.dep_id = b.dep_id
where b.value is null""")




# -- Сравнение всех записей в таблицах
query_2_3_2 = ("""select hcode_id, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, dir_id, kato_id, vids_id, duch_id, nod_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where	hcode_id in ('00018', '00019', '00020')
	and calc_rule = 'total_rejects'
	and %s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.dir_id, a.kato_id, a.vids_id, 
		a.duch_id, a.nod_id, a.depo_id, a.dep_id from (
select 	ind.hcode_id, ind.org_id, ind.dor_kod, ind.date_type_id, ind.metric_type_id, ind.cargo_type_id, 7 as val_type_id, ind.unit_id, ind.dt, 
		(ind.value - ind2.value) as value, ind.ss, ind.dir_id, ind.kato_id, ind.vids_id, ind.duch_id, ind.nod_id, ind.depo_id, ind.dep_id
		from dm_stg.calc_src_indicators_t ind 
		left join dm_stg.calc_src_indicators_t ind2 
			on (ind.hcode_id = ind2.hcode_id
				and ind.org_id = ind2.org_id
				and ind.dor_kod = ind2.dor_kod
				and ind.metric_type_id = ind2.metric_type_id
				and ind.cargo_type_id = ind2.cargo_type_id
				and ind.unit_id = ind2.unit_id
				and ind.duch_id = ind2.duch_id
				and ind.nod_id = ind2.nod_id
				and ind.depo_id = ind2.depo_id
				and ind.dep_id = ind2.dep_id
				and ind.ss = ind2.ss
				and ind2.val_type_id = 1
				and ind2.date_type_id = 3
				and to_char(ind.dt, 'YYYY-MM-DD') = to_char(ind2.dt+interval '1 day', 'YYYY-MM-DD'))
where ind.hcode_id in ('00018', '00019', '00020')
and ind.val_type_id = 1
and ind.date_type_id = 3 
and ind.%s)a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and val_type_id = 7
	and date_type_id = 3) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id
	and a.unit_id = b.unit_id
	and a.kato_id = b.kato_id 
	and a.vids_id = b.vids_id
	and a.depo_id = b.depo_id
	and a.dep_id = b.dep_id
where b.value is null""")



# -- АРМ


query_2_3_3 = ("""select 'tgt', count(0)
	from dm_rep.dm_all_indicators_v
where	ss = 'ARM'
and calc_rule = 'total_rejects'
and %s
union all
select 'src', count(0)	from (
select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, 3 as date_type_id, metric_type_id, cargo_type_id, 7 as val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_stg.calc_src_indicators_t ind 
where ss = 'ARM'
and val_type_id = 3
and date_type_id = 3
and %s)a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and val_type_id = 7
	and date_type_id = 3) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id
	and a.unit_id = b.unit_id
	and a.kato_id = b.kato_id 
	and a.vids_id = b.vids_id
	and a.depo_id = b.depo_id
	and a.dep_id = b.dep_id
where b.value is null""")


query_2_3_4 = ("""select hcode_id, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, vids_id, kato_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where	ss = 'ARM'
and calc_rule = 'total_rejects'
and %s
except
select 	a.hcode_id, a.org_id, a.dor_kod, a.date_type_id, a.metric_type_id, a.cargo_type_id, 
		a.val_type_id, a.unit_id, a.dt, a.value, a.ss, a.duch_id, a.nod_id, a.dir_id, a.vids_id, a.kato_id, a.depo_id, a.dep_id
from (
select 	ind.hcode_id, ind.org_id, ind.dor_kod, ind.date_type_id, ind.metric_type_id, ind.cargo_type_id, 7 as val_type_id, ind.unit_id, ind.dt, 
		(ind.value - ind2.value) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.kato_id, ind.vids_id, ind.depo_id, ind.dep_id
		from dm_stg.calc_src_indicators_t ind 
		left join dm_stg.calc_src_indicators_t ind2
			on (ind.hcode_id = ind2.hcode_id
				and ind.org_id = ind2.org_id
				and ind.dor_kod = ind2.dor_kod
				and ind.metric_type_id = ind2.metric_type_id
				and ind.cargo_type_id = ind2.cargo_type_id
				and ind.unit_id = ind2.unit_id
				and ind.duch_id = ind2.duch_id
				and ind.nod_id = ind2.nod_id
				and ind.depo_id = ind2.depo_id
				and ind.dep_id = ind2.dep_id
				and ind.ss = ind2.ss
				and ind2.val_type_id = 3
				and ind2.date_type_id = 3
				and to_char(ind.dt, 'YYYY-MM-DD') = to_char(ind2.dt+interval '1 day', 'YYYY-MM-DD'))
where ind.ss = 'ARM'
and ind.val_type_id = 3
and ind.date_type_id = 3
and ind.%s)a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from (select * from dm_rep.dm_all_indicators_v where vt = 'BASE') as ind 
        join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
		join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and val_type_id = 7
	and date_type_id = 3) b
on  	a.hcode_id = b.hcode_id
	and a.org_id = b.org_id
	and a.duch_id = b.duch_id
	and a.nod_id = b.nod_id
	and a.metric_type_id = b.metric_type_id
	and a.cargo_type_id = b.cargo_type_id
	and a.dt = b.dt
	and a.dir_id = b.dir_id
	and a.unit_id = b.unit_id
	and a.kato_id = b.kato_id 
	and a.vids_id = b.vids_id
	and a.depo_id = b.depo_id
	and a.dep_id = b.dep_id
where b.value is null""")

QUERYS_7_1 = [v for v in locals() if v.startswith('query')]


QUERYS_7_1_EQUAL = [n for n in QUERYS_7_1 if QUERYS_7_1.index(n) % 2 == 0]
QUERYS_7_1_EMPTY = [n for n in QUERYS_7_1 if QUERYS_7_1.index(n) % 2 != 0]