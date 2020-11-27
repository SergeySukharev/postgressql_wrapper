# --------------------------------------------------
# ---- Месяц. Расчетный поправочный коэффициент ----
# --------------------------------------------------

# CD where metric_type=17 and hcode=00012 / CD where metric_type=17 and hcode =00027 / CD where metric_type=17 and hcode=00011


# metric_type = 17 and hcode = 00012  Факт  Производительность локомотива рабочего парка в грузовом движении
# metryc_type = 17 and hcode = 00027  Факт  Среднесуточный пробег локомотива рабочего парка
# metric_type = 17 and hcode = 00011  Факт  Средний вес грузового поезда


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_5_2_1 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id in ('00035')
	and val_type_id in (5,7,9)
	and metric_type_id = 29 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30) a
		join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00027' and metric_type_id = 17 and unit_id = 19) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 and unit_id = 39) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать


# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_2 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id in ('00035') -- Расчетный поправочный коэффициент
	and val_type_id in (5,7,9)
	and metric_type_id = 29 -- Расчетный поправочный коэффициент
	and date_type_id = 4 -- Месяц
	and %s
except
select 	'00035' as hcode_id, 
		'Расчетный поправочный коэффициент' as hcode_name,
		'коэффициент' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		29 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		22 as unit_id, 
		a.dt as dt, 
		(a.value/nullif(b.value,0)/nullif(c.value,0)) as value,
		a.ss as ss, 
		a.duch_id,
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30) a
		join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00027' and metric_type_id = 17 and unit_id = 19) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 and unit_id = 39) c
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s""")

# -- Ожидаемый результат: Пустой вывод


# -----------------------------------------------------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении ----
# -----------------------------------------------------------------------------------------------------------------------------------------

# metric_type = 17 and hcode = 00012  Факт  Производительность локомотива рабочего парка в грузовом движении
# metryc_type = 12 and hcode = 00034  План  Грузооборот брутто (т-км брутто в грузовом движении)
# metric_type = 17 and hcode = 00033  Факт  Рабочий парк локомотивов	


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_5_2_3 = ("""select * from(
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id in ('00037') -- Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении
	and val_type_id in (5,7,9)
	and metric_type_id = 30 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00034' and metric_type_id = 12 and unit_id = 32) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00033' and metric_type_id = 17 and unit_id = 35) c
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id """)

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать


# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_4 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id in ('00037') -- Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении
	and val_type_id in (5,7,9)
	and metric_type_id = 30 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
except
select 	'00037' as hcode_id, 
		'Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении' as hcode_name,
		'тыс. ткм. бр.' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		30 as unit_id, 
		a.dt as dt, 
		(a.value - ((b.value)*1000/c.value)) as value,
		a.ss as ss, 
		a.duch_id, 
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00034' and metric_type_id = 12 and unit_id = 32) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00033' and metric_type_id = 17 and unit_id = 35) c
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта рабочего парка к плану на производительность локомотива рабочего парка в грузовом движении ----
# ------------------------------------------------------------------------------------------------------------------------------------


# metric_type = 17 and hcode = 00012  Факт  Производительность локомотива рабочего парка в грузовом движении
# metric_type = 17 and hcode = 00034  Факт  Грузооборот брутто (т-км брутто в грузовом движении)
# metric_type = 12 and hcode = 00033  План  Рабочий парк локомотивов


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_5_2_5 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'influence'
		and hcode_id in ('00038') -- Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении
		and val_type_id in (5,7,9)
		and metric_type_id = 30 -- Влияние
		and date_type_id = 4
		and %s
	group by val_type_id
	union all
	select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30 ) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00034' and metric_type_id = 17 and unit_id = 32 ) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00033' and metric_type_id = 12 and unit_id = 35 ) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
	where 	a.val_type_id in (5,7,9)
		and a.date_type_id = 4
		and a.%s
group by a.val_type_id
)al 
order by al.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать


# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_6 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id in ('00038') -- Влияние отклонения факта грузооборота брутто к плану на производительность локомотива рабочего парка в грузовом движении
	and val_type_id in (5,7,9)
	and metric_type_id = 30 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
except
select 	'00038' as hcode_id, 
		'Влияние отклонения факта рабочего парка к плану на производительность локомотива рабочего парка в грузовом движении' as hcode_name,
		'тыс. ткм. бр.' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		30 as unit_id, 
		a.dt as dt, 
		(a.value - (b.value/c.value)) as value,
		a.ss as ss, 
		a.duch_id, 
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 and unit_id = 30 ) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00034' and metric_type_id = 17 and unit_id = 32 ) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00033' and metric_type_id = 12 and unit_id = 35) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
	and a.date_type_id = 4 -- Месяц
	and a.val_type_id in (5,7,9)
	and a.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# -----------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта среднего состава поезда к плану на средний вес поезда ----
# -----------------------------------------------------------------------------------------------

# CD where metric_type=17 and hcode=00011 - (CD where metric_type=17 and hcode=00031)*(CD where metric_type=12 and hcode=00028)

# metric_type = 17 and hcode = 00011  Факт  Средний вес грузового поезда
# metric_type = 17 and hcode = 00031  Факт  Вес вагона
# metric_type = 12 and hcode = 00028  План  Средний состав поезда


# -- Сравнение количества записей в таблицах --
# --------------------------------------------- 
query_5_2_7 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'influence'
		and hcode_id = '00039' -- Влияние отклонения факта среднего состава поезда к плану на средний вес поезда
		and val_type_id in (5,7,9)
		and metric_type_id = 30 -- Влияние
		and date_type_id = 4
		and %s
	group by val_type_id
	union all
	select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00031' and metric_type_id = 17 /*and unit_id = 39*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 12 /*and unit_id = 69*/) c
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
	where 	a.val_type_id in (5,7,9)
		and a.date_type_id = 4
		and a.%s
group by a.val_type_id
)al 
order by al.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать


# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_8 = ("""select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
	and hcode_id = '00039' -- Влияние отклонения факта среднего состава поезда к плану на средний вес поезда
	and val_type_id in (5,7,9)
	and metric_type_id = 30 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
except
select 	'00039' as hcode_id, 
		'Влияние отклонения факта среднего состава поезда к плану на средний вес поезда' as hcode_name,
		'тонн' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		39 as unit_id, 
		a.dt as dt, 
		(a.value - (b.value*c.value)) as value,
		a.ss as ss,
		a.duch_id,
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00031' and metric_type_id = 17 /*and unit_id = 39*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 12 /*and unit_id = 69*/) c
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# -----------------------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта процента порожнего пробега к общему к плану на средний вес поезда ----
# -----------------------------------------------------------------------------------------------------------

# CD where metric_type=17 and hcode=00011 - (100% - CD where metric_type=12 and hcode=00032)*(CD where metric_type=17 and hcode=00036)/100 + (CD where metric_type=17 and hcode=00030)*(CD where metric_type=17 and hcode=00028)

# metric_type = 17 and hcode = 00011  Факт  Средний вес грузового поезда
# metric_type = 12 and hcode = 00032  План  Процент порожнего пробега к общему в грузовом движении
# metric_type = 17 and hcode = 00036  Факт  Средняя динамическая нагрузка на груженый вагон в грузовом движении
# metric_type = 17 and hcode = 00030  Факт  Вес тары
# metric_type = 17 and hcode = 00028  Факт  Средний состав поезда


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_5_2_9 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'influence'
		and hcode_id = '00040' -- Влияние отклонения факта процента порожнего пробега к общему к плану на средний вес поезда
		and val_type_id in (5,7,9)
		and metric_type_id = 30 -- Влияние
		and date_type_id = 4
		and %s
	group by val_type_id
	union all
	select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00032' and metric_type_id = 12 /*and unit_id = 46*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00036' and metric_type_id = 17 /*and unit_id = 39*/) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00030' and metric_type_id = 17 /*and unit_id = 39*/) d
			on (	a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 17 /*and unit_id = 69*/) e
			on (	a.org_id = e.org_id
				and a.date_type_id = e.date_type_id
				and a.cargo_type_id = e.cargo_type_id
				and a.val_type_id = e.val_type_id
				and a.dir_id = e.dir_id
				and a.duch_id = e.duch_id
				and a.nod_id = e.nod_id
and a.kato_id = e.kato_id
and a.vids_id = e.vids_id
and a.depo_id = e.depo_id
and a.dep_id = e.dep_id
				and a.dt = e.dt
				and a.kato_id = e.kato_id
				and a.vids_id = e.vids_id)
	where 	a.val_type_id in (5,7,9)
		and a.date_type_id = 4
		and a.%s
group by a.val_type_id
)al 
order by al.val_type_id""")
# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать
	

# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_10 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id = '00040' -- Влияние отклонения факта процента порожнего пробега к общему к плану на средний вес поезда
	and val_type_id in (5,7,9)
	and metric_type_id = 30 -- Влияние
	and date_type_id = 4 -- Месяц
	and %s
except
select 	'00040' as hcode_id, 
		'Влияние отклонения факта процента порожнего пробега к общему к плану на средний вес поезда' as hcode_name,
		'тонн' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		39 as unit_id, 
		a.dt as dt, 
		a.value - (100 - b.value)*c.value/100 + d.value*e.value as value,
		a.ss as ss,
		a.duch_id,
		a.nod_id, 
		a.dir_id, 
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00032' and metric_type_id = 12 /*and unit_id = 46*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00036' and metric_type_id = 17 /*and unit_id = 39*/) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00030' and metric_type_id = 17 /*and unit_id = 39*/) d
			on (	a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 17 /*and unit_id = 69*/) e
			on (	a.org_id = e.org_id
				and a.date_type_id = e.date_type_id
				and a.cargo_type_id = e.cargo_type_id
				and a.val_type_id = e.val_type_id
				and a.dir_id = e.dir_id
				and a.duch_id = e.duch_id
				and a.nod_id = e.nod_id
and a.kato_id = e.kato_id
and a.vids_id = e.vids_id
and a.depo_id = e.depo_id
and a.dep_id = e.dep_id
				and a.dt = e.dt
				and a.kato_id = e.kato_id
				and a.vids_id = e.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# ------------------------------------------------------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта средней динамической нагрузки на рабочий вагон в грузовом движении к плану на средний вес поезда ----
# ------------------------------------------------------------------------------------------------------------------------------------------

# CD where metric_type=17 and hcode=00011 - (CD where metric_type=17 and hcode=00030)*(CD where metric_type=12 and hcode=00029)*(CD where metric_type=17 and hcode=00028)

# metric_type = 17 and hcode = 00011  Факт  Средний вес грузового поезда
# metric_type = 17 and hcode = 00030  Факт  Вес тары
# metric_type = 12 and hcode = 00029  План  Средняя динамическая нагрузка на рабочий вагон в грузовом движении
# metric_type = 17 and hcode = 00028  Факт  Средний состав поезда


# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_5_2_11 = ("""select * from (
	select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'influence'
		and hcode_id = '00041' -- Влияние отклонения факта средней динамической нагрузки на рабочий вагон в грузовом движении к плану на средний вес поезда
		and val_type_id in (5,7,9)
		and metric_type_id = 30 -- Влияние
		and date_type_id = 4
		and %s
	group by val_type_id
	union all
	select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00030' and metric_type_id = 17 /*and unit_id = 39*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00029' and metric_type_id = 12 /*and unit_id = 39*/) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 17 /*and unit_id = 69*/) d
			on (	a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id)
	where 	a.date_type_id = 4 -- Месяц
		and a.val_type_id in (5,7,9)
		and a.%s
group by a.val_type_id
)al 
order by al.val_type_id""")

# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	
# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_12 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	hcode_id in ('00041') -- Влияние отклонения факта средней динамической нагрузки на рабочий вагон в грузовом движении к плану на средний вес поезда
	and val_type_id in (5,7,9)
	and metric_type_id = 30 
	and date_type_id = 4 
	and %s
except
select 	'00041' as hcode_id, 
		'Влияние отклонения факта средней динамической нагрузки на рабочий вагон в грузовом движении к плану на средний вес поезда' as hcode_name,
		'тонн' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		39 as unit_id, 
		a.dt as dt, 
		a.value - b.value*c.value*d.value as value,
		a.ss as ss, 
		a.duch_id,
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00030' and metric_type_id = 17 /*and unit_id = 39*/) b
			on (	a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00029' and metric_type_id = 12 /*and unit_id = 39*/) c
			on (	a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00028' and metric_type_id = 17 /*and unit_id = 69*/) d
			on (	a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id)
where 	a.val_type_id in (5,7,9)
	and a.date_type_id = 4 -- Месяц
	and a.%s""")
	
# -- Ожидаемый результат: Пустой вывод


# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ---- Месяц. Влияние отклонения факта среднесуточного пробега локомотива рабочего парка к плану на производительность локомотива рабочего парка в грузовом движении ----
# -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# CD where metric_type=17 and hcode=00012 - (CD where metric_type=17 and hcode=00011)*(CD where metric_type=a�and hcode=00035)*(CD where metric_type=12 and hcode=00027)/1000

# metric_type = 17 and hcode = 00011  
# metric_type = 17 and hcode = 00012  
# metric_type = 29 and hcode = 00035  
# metric_type = 12 and hcode = 00027  



# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_5_2_13 = ("""select * from (
	select 'calc', val_type_id, count(0) 
		from dm_rep.dm_all_indicators_v
	where 	calc_rule = 'influence'
		and hcode_id = '00042'
		and val_type_id in (5,7,9)
		and metric_type_id = 30 
		and date_type_id = 4
		and %s
	group by val_type_id
union all
	select 'join', a.val_type_id, count(0)
		from (	select * from dm_rep.dm_all_indicators_v where 	hcode_id = '00012' and metric_type_id = 17 /*and unit_id = 30*/) a
		left join (	select * from dm_rep.dm_all_indicators_v 
						where 	dm_rep.dm_all_indicators_v.hcode_id = '00011'
							and dm_rep.dm_all_indicators_v.metric_type_id = 17 
							--and dm_rep.dm_all_indicators_v.unit_id = 39
							) b
			on 		a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id
		left join (	select * from dm_rep.dm_all_indicators_v where hcode_id = '00035' and metric_type_id = 29 /*unit_id = 22*/) c
			on 		a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id
		left join (	select * from dm_rep.dm_all_indicators_v where hcode_id = '00027' and metric_type_id = 12 /*and dm_rep.dm_all_indicators_v.unit_id = 19*/) d
			on 		a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id
	where 	a.date_type_id = 4 
		and a.val_type_id in (5,7,9)
		and a.%s
	group by a.val_type_id
)al 
order by al.val_type_id""")
# -- Ожидаемый результат: Количество строк для 'join' и 'calc' должно совпадать

	
# -- Сравнение записей в таблицах --
# ----------------------------------
query_5_2_14 = ("""select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where 	calc_rule = 'influence'
		and hcode_id = '00042'
	and val_type_id in (5,7,9)
	and metric_type_id = 30 
	and date_type_id = 4
	and %s
except
select 	'00042' as hcode_id, 
		'Влияние отклонения факта среднесуточного пробега локомотива рабочего парка к плану на производительность локомотива рабочего парка в грузовом движении' as hcode_name,
		'тыс. ткм. бр.' as hcode_unit_name,
		a.org_id as org_id, 
		a.dor_kod as dor_kod, 
		a.date_type_id as date_type_id, 
		30 as metric_type_id, 
		a.cargo_type_id as cargo_type_id, 
		a.val_type_id as val_type_id, 
		30 as unit_id, 
		a.dt as dt, 
		a.value - b.value*c.value*d.value/1000 as value,
		a.ss as ss, 
		a.duch_id,
		a.nod_id, 
		a.dir_id,
		a.kato_id,
		a.vids_id,
		a.depo_id,
		a.dep_id
	from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 17 /*and unit_id = 30*/) a
	left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00011' and metric_type_id = 17 /*and unit_id = 39*/) b
		on (		a.org_id = b.org_id
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt
				and a.kato_id = b.kato_id
				and a.vids_id = b.vids_id)
	left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00035' and metric_type_id = 29 /*and unit_id = 22*/) c
		on (		a.org_id = c.org_id
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt
				and a.kato_id = c.kato_id
				and a.vids_id = c.vids_id)
	left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00027' and metric_type_id = 12 /*and unit_id = 19*/) d
		on (		a.org_id = d.org_id
				and a.date_type_id = d.date_type_id
				and a.cargo_type_id = d.cargo_type_id
				and a.val_type_id = d.val_type_id
				and a.dir_id = d.dir_id
				and a.duch_id = d.duch_id
				and a.nod_id = d.nod_id
and a.kato_id = d.kato_id
and a.vids_id = d.vids_id
and a.depo_id = d.depo_id
and a.dep_id = d.dep_id
				and a.dt = d.dt
				and a.kato_id = d.kato_id
				and a.vids_id = d.vids_id)
where 	a.date_type_id = 4
	and a.val_type_id in (5,7,9)
	and a.%s""")
# -- Ожидаемый результат: Пустой вывод

QUERYS_5_2 = [v for v in locals() if v.startswith('query')]

QUERYS_5_2_EQUAL = [n for n in QUERYS_5_2 if QUERYS_5_2.index(n) % 2 != 0]
QUERYS_5_2_EMPTY = [n for n in QUERYS_5_2 if QUERYS_5_2.index(n) % 2 == 0]
