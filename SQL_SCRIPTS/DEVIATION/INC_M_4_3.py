# ------------------------------------------------------------
# ---- Квартал. Отклонение факта к факту прошлого года, % ----
# ------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_1 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 21
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', cd.val_type_id, count(0) from (select * from dm_rep.dm_all_indicators_v) cd
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
	where 	cd.val_type_id in (4,7) 
		and cd.metric_type_id = 17
		and cd.date_type_id = 2 
		and cd.%s
	group by cd.val_type_id
)a 
order by val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать



# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_2 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id  
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)	
	and metric_type_id = 21 
	and date_type_id = 2 
	and %s
except
select 	cd.hcode_id, hcd.name, hcd.unit_name, cd.org_id, cd.dor_kod, cd.date_type_id, 21 as metric_type_id, cd.cargo_type_id, 
		cd.val_type_id, cd.unit_id, cd.dt, (cd.value - pyd.value)/abs(case when pyd.value = 0 
		then null else pyd.value end)*100, cd.ss, cd.duch_id, cd.nod_id, cd.dir_id, cd.kato_id, cd.vids_id, cd.depo_id, cd.dep_id
		from (select * from dm_rep.dm_all_indicators_v) cd
        join dm_rep.d_hcode_v hcd on cd.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
where 	cd.val_type_id in (4,7)	
	and cd.metric_type_id = 17 
	and cd.date_type_id = 2 
	and cd.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# --------------------------------------------------------------------------------------------
# ---- Квартал. Отклонение факта расследованного к факту расследованному прошлого года, % ----
# --------------------------------------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_3 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 120
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', cd.val_type_id, count(0) from (select * from dm_rep.dm_all_indicators_v) cd
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
	where 	cd.val_type_id in (4,7) 
		and cd.metric_type_id = 1
		and cd.date_type_id = 2 
		and cd.%s
	group by cd.val_type_id
)a 
order by val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать



# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_4 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)	
	and metric_type_id = 120
	and date_type_id = 2 	
	and %s
except
select 	cd.hcode_id, hcd.name, hcd.unit_name, cd.org_id, cd.dor_kod, cd.date_type_id, 120 as metric_type_id, cd.cargo_type_id, 
		cd.val_type_id, cd.unit_id, cd.dt, (cd.value - pyd.value)/abs(case when pyd.value = 0 
		then null else pyd.value end)*100, cd.ss, cd.duch_id, cd.nod_id, cd.dir_id, cd.kato_id, cd.vids_id, cd.depo_id, cd.dep_id
		from (select * from dm_rep.dm_all_indicators_v) cd
        join dm_rep.d_hcode_v hcd on cd.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
where 	cd.val_type_id in (4,7)	
	and cd.metric_type_id = 1
	and cd.date_type_id = 2 	
	and cd.%s""")
	
# -- Ожидаемый результат: Пустой вывод

# --------------------------------------------
# ---- Квартал. Отклонение факта к плану, % ----
# --------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_4_3_5 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 22 -- Отклонение факта к плану, процент
	and date_type_id = 2
	and %s
group by val_type_id
union all
select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2
	and fct.%s
group by fct.val_type_id
) a order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_6 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 22 -- Отклонение факта к плану, процент
	and date_type_id = 2 
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 22 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, (fct.value - pln.value)
		/abs(case when pln.value = 0 then null else pln.value end)*100, fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln 
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2 
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# ---------------------------------------------------------
# ---- Квартал. Отклонение факта к директивному плану, % ----
# ---------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_7 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 23 -- Отклонение факта к директивному плану, процент
		and date_type_id = 2 
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_8 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id  
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 23 -- Отклонение факта к директивному плану, процент
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 23 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, (fct.value - pln.value)/abs(case when pln.value = 0 
		then null else pln.value end)*100, fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2 
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------------------------
# ---- Квартал. Абсолютное отклонение факта к факту прошлого года ----
# ------------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_9 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 28 -- Абсолютное отклонение факта к факту прошлого года
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', cd.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v) cd
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
	where 	cd.val_type_id in (4,7)	
		and cd.metric_type_id = 17 	-- Факт
		and cd.date_type_id = 2 
		and cd.%s
	group by cd.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать



# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_10 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 28 -- Абсолютное отклонение факта к факту прошлого года
	and date_type_id = 2 
	and %s
except
select 	cd.hcode_id, hcd.name, hcd.unit_name, cd.org_id, cd.dor_kod, cd.date_type_id, 28 as metric_type_id, cd.cargo_type_id, 
		cd.val_type_id, cd.unit_id, cd.dt, (cd.value - pyd.value), cd.ss, cd.duch_id, cd.nod_id, cd.dir_id, cd.kato_id, cd.vids_id, cd.depo_id, cd.dep_id
		from (select * from dm_rep.dm_all_indicators_v) cd
        join dm_rep.d_hcode_v hcd on cd.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt) +1)
where 	cd.val_type_id in (4,7)	
	and cd.metric_type_id = 17 	-- Абсолютное отклонение факта к факту прошлого года
	and cd.date_type_id = 2 
	and cd.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------------------------
# ---- Квартал. Абсолютное отклонение факта расследованного к факту расследованному прошлого года ----
# ------------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_11 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 117
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', cd.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v) cd
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt)+1)
	where 	cd.val_type_id in (4,7)	
		and cd.metric_type_id = 1 	
		and cd.date_type_id = 2 
		and cd.%s
	group by cd.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать



# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_12 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 117
	and date_type_id = 2 
	and %s
except
select 	cd.hcode_id, hcd.name, hcd.unit_name, cd.org_id, cd.dor_kod, cd.date_type_id, 117 as metric_type_id, cd.cargo_type_id, 
		cd.val_type_id, cd.unit_id, cd.dt, (cd.value - pyd.value), cd.ss, cd.duch_id, cd.nod_id, cd.dir_id, cd.kato_id, cd.vids_id, cd.depo_id, cd.dep_id
		from (select * from dm_rep.dm_all_indicators_v) cd
        join dm_rep.d_hcode_v hcd on cd.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v) pyd
			on (	cd.hcode_id = pyd.hcode_id
				and cd.org_id = pyd.org_id
				and cd.dor_kod = pyd.dor_kod
				and cd.date_type_id = pyd.date_type_id
				and cd.metric_type_id = pyd.metric_type_id
				and cd.cargo_type_id = pyd.cargo_type_id
				and cd.val_type_id = pyd.val_type_id
				and cd.unit_id = pyd.unit_id
				and cd.dir_id = pyd.dir_id
				--and cd.ss = pyd.ss
				and cd.duch_id = pyd.duch_id
and cd.depo_id = pyd.depo_id
and cd.dep_id = pyd.dep_id
				and cd.nod_id = pyd.nod_id
				and date_part('month', cd.dt) = date_part('month', pyd.dt)
				and date_part('day', cd.dt) = date_part('day', pyd.dt)
				and date_part('year', cd.dt) = date_part('year', pyd.dt) +1)
where 	cd.val_type_id in (4,7)	
	and cd.metric_type_id = 1
	and cd.date_type_id = 2 
	and cd.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# -----------------------------------------------------------------
# ---- Квартал. Абсолютное отклонение факта оперативного к плану ----
# -----------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_13 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 25 -- Абсолютное отклонение факта оперативного к плану
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_14 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 25 -- Абсолютное отклонение факта оперативного к плану
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 25 as metric_type_id, fct.cargo_type_id, 
		fct.val_type_id, fct.unit_id, fct.dt, (fct.value - pln.value), fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------------------------------------
# ---- Квартал. Абсолютное отклонение факта оперативного к директивному плану ----
# ------------------------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_15 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 24 -- Абсолютное отклонение факта оперативного к директивному плану
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln 
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2 
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_16 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 24 -- Абсолютное отклонение факта оперативного к директивному плану
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 24 as metric_type_id, fct.cargo_type_id, 
		fct.val_type_id, fct.unit_id, fct.dt, (fct.value - pln.value), fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln 
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2 
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# -----------------------------------
# ---- Квартал. Выполнение плана ----
# -----------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_17 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 26 -- Выполнение плана
		and date_type_id = 2
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2 
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_18 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 26 -- Выполнение плана
	and date_type_id = 2 
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 26 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, fct.value/(case when pln.value = 0 then null else pln.value end)*100, 
		fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)-- Итог
	and fct.date_type_id = 2 
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------
# ---- Квартал. Выполнение директивного плана ----
# ------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_19 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 27 -- Выполнение директивного плана
		and date_type_id = 2 
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_20 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 27 -- Выполнение директивного плана
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 27 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, fct.value/abs(case when pln.value = 0 then null else pln.value end)*100, 
		fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 2) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


# -------------------------------------
# ---- Квартал. Доля от плана года ----
# -------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_4_3_21 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and metric_type_id = 42 
	and date_type_id = 2
	and %s
group by val_type_id
union all
select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17 and date_type_id = 2) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12 and date_type_id = 5 and val_type_id = 7) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.cargo_type_id = pln.cargo_type_id
				--and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				and fct.kato_id = pln.kato_id
				and fct.vids_id = pln.vids_id
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and date_trunc('year',fct.dt) = date_trunc('year',pln.dt))
			join dm.d_hcode_t hcd on hcd.id = fct.hcode_id
where 	fct.val_type_id in (7,4)
		and hcd.group_name = 'Обеспеченность ремонтно-путевых работ путевой техникой и подвижным составом'
		and fct.%s
group by fct.val_type_id
) a order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_22 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and metric_type_id = 42
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 42 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, (fct.value/pln.value)*100 as value, fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
	from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17 and date_type_id = 2) fct
    join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
	left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12 and date_type_id = 5 and val_type_id = 7) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.cargo_type_id = pln.cargo_type_id
				--and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				and fct.kato_id = pln.kato_id
				and fct.vids_id = pln.vids_id
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and date_trunc('year',fct.dt) = date_trunc('year',pln.dt))
where 	fct.val_type_id in (7,4)
		and hcd.group_name = 'Обеспеченность ремонтно-путевых работ путевой техникой и подвижным составом'
		and fct.%s""")


# -- Ожидаемый результат: Пустой вывод

# ----------------------------------------------
# ---- Квартал. Отклонение факта к плану, % ----
# ----------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_4_3_23 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 201 -- Отклонение плана к факту прошлого года, процент
	and date_type_id = 2
    and %s
group by val_type_id
union all
select 'join', pln.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				and fct.kato_id = pln.kato_id
				and fct.vids_id = pln.vids_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and pln.dt = fct.dt + interval '1 year')
where 	pln.val_type_id in (4,7)
	and pln.date_type_id = 2
    and pln.%s
group by pln.val_type_id
) a order by a.val_type_id""")
# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------


query_4_3_24 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 201 -- Отклонение плана к факту прошлого года, процент
	and date_type_id = 2 
    and %s
except
select 	pln.hcode_id, hcd.name, hcd.unit_name, pln.org_id, pln.dor_kod, pln.date_type_id, 201 as metric_type_id, 
		pln.cargo_type_id, pln.val_type_id, pln.unit_id, pln.dt, (pln.value - fct.value)
		/abs(case when fct.value = 0 then null else fct.value end)*100, pln.ss, pln.duch_id, pln.nod_id, pln.dir_id, pln.kato_id, pln.vids_id, pln.depo_id, pln.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 12) pln
        join dm_rep.d_hcode_v hcd on pln.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct 
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and pln.dt = fct.dt + interval '1 year')
where 	pln.val_type_id in (4,7)
	and pln.date_type_id = 2
    and pln.%s""")

# -- Ожидаемый результат: Пустой вывод


# ------------------------------
# ---- Квартал. Доля в сети ----
# ------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_4_3_25 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
		where 	calc_rule = 'deviation'
			and metric_type_id = 202
			and date_type_id = 2 
            and %s
	group by val_type_id
	union all
	select 'join', st.val_type_id, count(0) from (
		select * from dm_rep.dm_all_indicators_v
		where 	val_type_id in (4,7)	
			and metric_type_id = 17
			and date_type_id = 2
			and dor_kod in (1,10,17,24,28,51,58,61,63,76,80,83,88,92,94,96 ) 
            and %s 
            ) st
		left join (select * from dm_rep.dm_all_indicators_v where dor_kod = 41) dor
			on (	st.hcode_id = dor.hcode_id
				and st.date_type_id = dor.date_type_id
				and st.metric_type_id = dor.metric_type_id
				and st.cargo_type_id = dor.cargo_type_id
				and st.val_type_id = dor.val_type_id
				and st.unit_id = dor.unit_id
				and st.duch_id = dor.duch_id
				and st.nod_id = dor.nod_id
				and st.kato_id = dor.kato_id
				and st.vids_id = dor.vids_id
				and st.dir_id = dor.dir_id
				and st.dt = dor.dt)
	group by st.val_type_id
)a 
order by a.val_type_id""")


# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_4_3_26 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value::numeric(20,8), ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and metric_type_id = 202
	and date_type_id = 2 
    and %s
except
select 	dor.hcode_id, hcd.name, hcd.unit_name, dor.org_id, dor.dor_kod, dor.date_type_id, '202' as metric_type_id, 
		dor.cargo_type_id, dor.val_type_id, dor.unit_id, dor.dt, 
		((dor.value/case when st.value = 0 then null else st.value end)*100)::numeric(20,8) as value, 
		dor.ss, dor.duch_id, dor.nod_id, dor.dir_id, dor.kato_id, dor.vids_id, dor.depo_id, dor.dep_id
from
(select * from dm_rep.dm_all_indicators_v
	where 	val_type_id in (4,7)	
		and metric_type_id = 17
		and date_type_id = 2
		and dor_kod in (1,10,17,24,28,51,58,61,63,76,80,83,88,92,94,96 )
        and %s) dor
join dm_rep.d_hcode_v hcd on dor.hcode_id = hcd.id
left join (select * from dm_rep.dm_all_indicators_v where dor_kod = 41) st
			on (	st.hcode_id = dor.hcode_id
				and st.date_type_id = dor.date_type_id
				and st.metric_type_id = dor.metric_type_id
				and st.cargo_type_id = dor.cargo_type_id
				and st.val_type_id = dor.val_type_id
				and st.unit_id = dor.unit_id
				and st.duch_id = dor.duch_id
				and st.dir_id = dor.dir_id
				and st.nod_id = dor.nod_id
				and st.kato_id = dor.kato_id
				and st.vids_id = dor.vids_id
				and st.dt = dor.dt)""")

	
# -- Ожидаемый результат: Пустой вывод

# ---------------------------------------------------------------
# ---- Квартал. Отклонение факта к плану с корректировкой, % ----
# ---------------------------------------------------------------


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_4_3_27 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'deviation'
		and val_type_id in (4,7)
		and metric_type_id = 204 -- Отклонение факта к плану с корректировкой, процент
		and date_type_id = 2 
		and %s
	group by val_type_id
	union all
	select 'join', fct.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 18) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
	where 	fct.val_type_id in (4,7)
		and fct.date_type_id = 2
		and fct.%s
	group by fct.val_type_id
)a 
order by a.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	

# -- Сравнение записей в таблицах --
# ----------------------------------

query_4_3_28 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, 
		dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id  
	from dm_rep.dm_all_indicators_v
where 	calc_rule = 'deviation'
	and val_type_id in (4,7)
	and metric_type_id = 204 -- Отклонение факта к плану с корректировкой, процент
	and date_type_id = 2
	and %s
except
select 	fct.hcode_id, hcd.name, hcd.unit_name, fct.org_id, fct.dor_kod, fct.date_type_id, 204 as metric_type_id, 
		fct.cargo_type_id, fct.val_type_id, fct.unit_id, fct.dt, (fct.value - pln.value)/abs(case when pln.value = 0 
		then null else pln.value end)*100, fct.ss, fct.duch_id, fct.nod_id, fct.dir_id, fct.kato_id, fct.vids_id, fct.depo_id, fct.dep_id
		from (select * from dm_rep.dm_all_indicators_v where metric_type_id = 17) fct
        join dm_rep.d_hcode_v hcd on fct.hcode_id = hcd.id
		left join (select * from dm_rep.dm_all_indicators_v where metric_type_id = 18) pln
			on (	fct.hcode_id = pln.hcode_id
				and fct.org_id = pln.org_id
				and fct.dor_kod = pln.dor_kod
				and fct.date_type_id = pln.date_type_id
				and fct.cargo_type_id = pln.cargo_type_id
				and fct.val_type_id = pln.val_type_id
				and fct.unit_id = pln.unit_id
				and fct.dir_id = pln.dir_id
				--and fct.ss = pln.ss
				and fct.duch_id = pln.duch_id
				and fct.nod_id = pln.nod_id
and fct.depo_id = pln.depo_id
and fct.dep_id = pln.dep_id
				and fct.dt = pln.dt)
where 	fct.val_type_id in (4,7)
	and fct.date_type_id = 2 
	and fct.%s""")

# -- Ожидаемый результат: Пустой вывод


QUERYS_4_3 = [v for v in locals() if v.startswith('query')]

QUERYS_4_3_EQUAL = [n for n in QUERYS_4_3 if QUERYS_4_3.index(n) % 2 == 0]
QUERYS_4_3_EMPTY = [n for n in QUERYS_4_3 if QUERYS_4_3.index(n) % 2 != 0]