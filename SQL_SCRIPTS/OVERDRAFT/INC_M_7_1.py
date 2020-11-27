
# --------------------------------------------
# -----------------СУТКИ----------------------
# --------------------------------------------

# --Сутки. hcode  '00293'

# --CD where metric_type =17 and hcode=00141 - (CD where metric_type=17 and hcode=00291 *1000 / CD where metric_type=12 and hcode=00224). Если одной из составляющих нет, то NULL

# -- Сравнение количества записей в таблицах --
# ---------------------------------------------
query_7_1_1 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where hcode_id in ('00293')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200
	and date_type_id = 3 -- Сутки
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00141' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00291' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00224' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id""")

# -- Сравнение записей в таблицах --
# ----------------------------------

query_7_1_2 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id in ('00293')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200 
	and date_type_id = 3 -- Сутки
	and %s
except
select 	'00293' as hcode_id, 
		'Величина пересодержания локомотивов рабочего парка на фактически выполненный объем работы.Тепловозы' as hcode_name, 'тяг.ед.' as hcode_unit_name, a.org_id as org_id, a.dor_kod as dor_kod, a.date_type_id as date_type_id, 200 as metric_type_id, a.cargo_type_id as cargo_type_id,
		a.val_type_id as val_type_id, a.unit_id as unit_id, a.dt as dt, (a.value - nullif(b.value,0) * 1000/nullif(c.value,0)) as value, a.ss as ss, a.duch_id, a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00141' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00291' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00224' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and 	a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s""")

# --Сутки. hcode  '00294'

# --CD where metric_type =17 and hcode=00139 - (CD where metric_type=17 and hcode=00292 *1000 / CD where metric_type=12 and hcode=00224). Если одной из составляющих нет, то null

# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_7_1_3 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where hcode_id in ('00294')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200
	and date_type_id = 3 -- Сутки
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00139' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00292' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00224' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать

# -- Сравнение записей в таблицах --
# ----------------------------------

query_7_1_4 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id in ('00294')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200 
	and date_type_id = 3 -- Сутки
	and %s
except
select 	'00294' as hcode_id, 
		'Величина пересодержания локомотивов рабочего парка на фактически выполненный объем работы.Электровозы' as hcode_name, 'тяг.ед.' as hcode_unit_name, a.org_id as org_id, a.dor_kod as dor_kod, a.date_type_id as date_type_id, 200 as metric_type_id, a.cargo_type_id as cargo_type_id,
		a.val_type_id as val_type_id, a.unit_id as unit_id, a.dt as dt, (a.value - nullif(b.value,0) * 1000/nullif(c.value,0)) as value, a.ss as ss, a.duch_id, a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00139' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00292' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00224' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and 	a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s""")

# -- Ожидаемый результат: Пустой вывод


# --Сутки. hcode  '00295'

# --CD where metric_type =17 and hcode=00138 - (CD where metric_type=17 and hcode=00291 *1000 / CD where metric_type=12 and hcode=00012). Если одной из составляющих нет, то NULL

# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_7_1_5 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where hcode_id in ('00295')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200
	and date_type_id = 3 -- Сутки
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00138' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00291' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать

# -- Сравнение записей в таблицах --
# ----------------------------------

query_7_1_6 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id in ('00295')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200 
	and date_type_id = 3 -- Сутки
	and %s
except
select 	'00295' as hcode_id, 
		'Величина пересодержания локомотивов эксплуатируемого парка на фактически выполненный объем работы.Тепловозы' as hcode_name, 'тяг.ед.' as hcode_unit_name, a.org_id as org_id, a.dor_kod as dor_kod, a.date_type_id as date_type_id, 200 as metric_type_id, a.cargo_type_id as cargo_type_id,
		a.val_type_id as val_type_id, a.unit_id as unit_id, a.dt as dt, (a.value - nullif(b.value,0) * 1000/nullif(c.value,0)) as value, a.ss as ss, a.duch_id, a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00138' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00291' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and 	a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s""")

# -- Ожидаемый результат: Пустой вывод


# --Сутки. hcode  '00296'

# --CD where metric_type =17 and hcode=00144 - (CD where metric_type=17 and hcode=00292 *1000 / CD where metric_type=12 and hcode=00012). Если одной из составляющих нет, то NULL

# -- Сравнение количества записей в таблицах --
# ---------------------------------------------

query_7_1_7 = ("""select * from (
select 'calc', val_type_id, count(0) from dm_rep.dm_all_indicators_v
where hcode_id in ('00296')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200
	and date_type_id = 3 -- Сутки
	and %s
group by val_type_id
union all
select 'join', a.val_type_id, count(0)
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00144' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00292' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s
group by a.val_type_id
) al
order by al.val_type_id""")

# -- Ожидаемый результат: количество строк для 'join' и 'calc' должно совпадать

# -- Сравнение записей в таблицах --
# ----------------------------------

query_7_1_8 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, 
		val_type_id, unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id in ('00296')
	and val_type_id in (1,3,7,8)
	and metric_type_id = 200 
	and date_type_id = 3 -- Сутки
	and %s
except
select 	'00296' as hcode_id, 
		'Величина пересодержания локомотивов эксплуатируемого парка на фактически выполненный объем работы.Электровозы' as hcode_name, 'тяг.ед.' as hcode_unit_name, a.org_id as org_id, a.dor_kod as dor_kod, a.date_type_id as date_type_id, 200 as metric_type_id, a.cargo_type_id as cargo_type_id,
		a.val_type_id as val_type_id, a.unit_id as unit_id, a.dt as dt, (a.value - nullif(b.value,0) * 1000/nullif(c.value,0)) as value, a.ss as ss, a.duch_id, a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
		from (select * from dm_rep.dm_all_indicators_v where hcode_id = '00144' and metric_type_id = 17) a
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00292' and metric_type_id = 17) b
			on (	a.org_id = b.org_id
				and a.dor_kod = b.dor_kod
				and a.date_type_id = b.date_type_id
				and a.cargo_type_id = b.cargo_type_id
				and a.val_type_id = b.val_type_id
				and a.dir_id = b.dir_id
				and a.unit_id = b.unit_id
				--and a.ss = b.ss
				and a.duch_id = b.duch_id
				and a.nod_id = b.nod_id
and a.kato_id = b.kato_id
and a.vids_id = b.vids_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
				and a.dt = b.dt)
		left join (select * from dm_rep.dm_all_indicators_v where hcode_id = '00012' and metric_type_id = 12) c
			on (	a.org_id = c.org_id
				and a.dor_kod = c.dor_kod
				and 	a.date_type_id = c.date_type_id
				and a.cargo_type_id = c.cargo_type_id
				and a.val_type_id = c.val_type_id
				and a.dir_id = c.dir_id
				and a.unit_id = c.unit_id
				--and a.ss = c.ss
				and a.duch_id = c.duch_id
				and a.nod_id = c.nod_id
and a.kato_id = c.kato_id
and a.vids_id = c.vids_id
and a.depo_id = c.depo_id
and a.dep_id = c.dep_id
				and a.dt = c.dt)
where 	a.val_type_id in (1, 3, 7, 8)
	and a.date_type_id = 3 -- Сутки
	and a.%s""")

# -- Ожидаемый результат: Пустой вывод

QUERYS_7_1 = [v for v in locals() if v.startswith('query')]

QUERYS_7_1_EQUAL = [n for n in QUERYS_7_1 if QUERYS_7_1.index(n) % 2 != 0]
QUERYS_7_1_EMPTY = [n for n in QUERYS_7_1 if QUERYS_7_1.index(n) % 2 == 0]
