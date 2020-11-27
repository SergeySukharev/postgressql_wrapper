
# -- hcode '00110'

query_3_25 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00110'
and calc_rule = 'ratio'
and %s
union all
select count(0) from (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id in (12,17,1,2,10)) a
				left join (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id in (12,17,1,2,10)) b
					on (a.metric_type_id = b.metric_type_id
						and a.org_id = b.org_id
						and a.dor_kod = b.dor_kod
						and a.date_type_id = b.date_type_id	
						and a.cargo_type_id = b.cargo_type_id
						and a.val_type_id = b.val_type_id
						and a.dt = b.dt
						and a.nod_id = b.nod_id
						and a.duch_id = b.duch_id
                        and a.depo_id = b.depo_id
                        and a.dep_id = b.dep_id
                        and a.kato_id = b.kato_id
                        and a.vids_id = b.vids_id)
				left join (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id in (12,17,1,2,10)) c
					on (a.metric_type_id = c.metric_type_id
						and a.org_id = c.org_id
						and a.dor_kod = c.dor_kod
						and a.date_type_id = c.date_type_id	
						and a.cargo_type_id = c.cargo_type_id
						and a.val_type_id = c.val_type_id
						and a.dt = c.dt
						and a.nod_id = c.nod_id
						and a.duch_id = c.duch_id
                        and a.depo_id = c.depo_id
                        and a.dep_id = c.dep_id
                        and a.kato_id = c.kato_id
                        and a.vids_id = c.vids_id)
left join (select  * from dm_stg.calc_src_indicators_t ind
				join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
				join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
				where hcode_id = '00110' 
				and hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
			) d
    on  a.org_id = d.org_id 
	and a.duch_id = d.duch_id
	and a.nod_id = d.nod_id 
	and a.date_type_id = d.date_type_id
	and a.metric_type_id = d.metric_type_id
	and a.cargo_type_id = d.cargo_type_id
	and a.val_type_id = d.val_type_id 
	and a.dt = d.dt
	and a.dir_id = d.dir_id
    and a.depo_id = d.depo_id
    and a.dep_id = d.dep_id
    and a.kato_id = d.kato_id
    and a.vids_id = d.vids_id
where d.org_id is null          
    and a.%s""")


query_3_26 = ("""select 	'00110' as hcode_id, 'Потери поездо-часов, вызванных отказами 3 категории' as hcode_name, 'поездо-час' as hcode_unit_id, a.org_id, a.dor_kod, 
		a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, '48' as unit_id, a.dt, (coalesce(a.value,0)+coalesce(b.value,0)+coalesce(c.value,0)) as value, 
		a.ss, a.duch_id, a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
				from (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id in (12,17,1,2,10)) a
				left join (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id in (12,17,1,2,10)) b
					on (a.metric_type_id = b.metric_type_id
						and a.org_id = b.org_id
						and a.dor_kod = b.dor_kod
						and a.date_type_id = b.date_type_id	
						and a.cargo_type_id = b.cargo_type_id
						and a.val_type_id = b.val_type_id
						and a.dt = b.dt
						and a.nod_id = b.nod_id
						and a.duch_id = b.duch_id
                        and a.depo_id = b.depo_id
                        and a.dep_id = b.dep_id
                        and a.kato_id = b.kato_id
                        and a.vids_id = b.vids_id)	
				left join (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id in (12,17,1,2,10)) c
					on (a.metric_type_id = c.metric_type_id
						and a.org_id = c.org_id
						and a.dor_kod = c.dor_kod
						and a.date_type_id = c.date_type_id	
						and a.cargo_type_id = c.cargo_type_id
						and a.val_type_id = c.val_type_id
						and a.dt = c.dt
						and a.nod_id = c.nod_id
						and a.duch_id = c.duch_id
                        and a.depo_id = c.depo_id
                        and a.dep_id = c.dep_id
                        and a.kato_id = c.kato_id
                        and a.vids_id = c.vids_id)
left join (select  * from dm_stg.calc_src_indicators_t ind
				join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t) hcp on ind.hcode_id = hcp.hid
				join (select hcode_id as hid, src, priority from dm_lgc.m_hcode_priority_t where src = 'CALC') hcpr on hcp.hid = hcpr.hid
				where hcode_id = '00110' 
				and hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
			) d
    on  a.org_id = d.org_id 
	and a.duch_id = d.duch_id
	and a.nod_id = d.nod_id 
	and a.date_type_id = d.date_type_id
	and a.metric_type_id = d.metric_type_id
	and a.cargo_type_id = d.cargo_type_id
	and a.val_type_id = d.val_type_id 
	and a.dt = d.dt
	and a.dir_id = d.dir_id
    and a.depo_id = d.depo_id
    and a.dep_id = d.dep_id
    and a.kato_id = d.kato_id
    and a.vids_id = d.vids_id
where d.org_id is null 
    and a.%s
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00110'
and calc_rule = 'ratio'
and %s""")



# -- hcode '00112'

query_3_27 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00112'
and unit_id = 44
and metric_type_id in (12,2,17,1,10)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00203'
and metric_type_id in (12,2,17,1,10)
and unit_id = 4
and calc_rule = 'ratio'
and %s""")


query_3_28 = ("""select 	'00203' as hcode_id, 'Предоставление "окон", продолжительность (час)' as hcode_name, 'час' as hcode_unit_id, a.org_id, a.dor_kod, 
		a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, '4' as unit_id, a.dt, (a.value/60) as value, a.ss, a.duch_id, 
		a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
				from (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00112') and metric_type_id in (12,2,17) and unit_id = 44) a
		where a.%s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00203'
and unit_id = 4
and calc_rule = 'ratio'
and %s""")



query_3_31 = ("""select 	'00204' as hcode_id, 'Начисленная выручка от перевозочных видов деятельности (млрд.руб.)' as hcode_name, 'млрд.руб.' as hcode_unit_id, a.org_id, a.dor_kod, 
		a.date_type_id, a.metric_type_id, a.cargo_type_id, a.val_type_id, '25' as unit_id, a.dt, (a.value/1000) as value, a.ss, a.duch_id, 
		a.nod_id, a.dir_id, a.kato_id, a.vids_id, a.depo_id, a.dep_id
				from (select * from dm_rep.dm_all_indicators_v where hcode_id in ('00006') and metric_type_id in (12,2,17,1,10) and unit_id = 40) a
		where a.%s		
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00204'
and calc_rule = 'ratio'
and %s""")


# -- hcode 00215

query_3_32 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00109'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00215'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


# -- hcode '00204'

query_3_30 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00006'
and unit_id = 40
and metric_type_id in (12,2,17,1,10)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00204'
and metric_type_id in (12,2,17,1,10)
and unit_id = 25
and calc_rule = 'ratio'
and %s""")




query_3_33 = ("""select 	'00215' as hcode_id, 'Потери поездо-часов, вызванных отказами 1, 2 категории (поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00109'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00215'
and metric_type_id in (1,12,17)
and %s""")



# -- hcode 00217

query_3_36 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00111'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00217'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_37 = ("""select 	'00217' as hcode_id, 'Потери поездо-часов, вызванных технологическими нарушениями (поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00111'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00217'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00218

query_3_38 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00165'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00218'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_39 = ("""select 	'00218' as hcode_id, 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (грузовые, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00165'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00218'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00219

query_3_40 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00166'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00219'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_41 = ("""select 	'00219' as hcode_id, 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (пассажирские, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00166'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00219'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00220

query_3_42 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00167'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00220'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_43 = ("""select 	'00220' as hcode_id, 'Потери поездо-часов из-за отказов 1, 2 категории по типу поездов (пригородные, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00167'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00220'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00221

query_3_44 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00168'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00221'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_45 = ("""select 	'00221' as hcode_id, 'Потери поездо-часов из-за отказов 3 категории по типу поездов (грузовые, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00168'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00221'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00222

query_3_46 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00169'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00222'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_47 = ("""select 	'00222' as hcode_id, 'Потери поездо-часов из-за отказов 3 категории по типу поездов (пассажирские, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00169'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00222'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00223

query_3_48 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00170'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00223'
and unit_id = 48
and metric_type_id in (1,12,17)
and %s""")


query_3_49 = ("""select 	'00223' as hcode_id, 'Потери поездо-часов из-за отказов 3 категории по типу поездов (пригородные, поездо-час)' as hcode_name, 'поездо-час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '48' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00170'
and ss = 'SAS'
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00223'
and metric_type_id in (1,12,17)
and %s""")


# -- hcode 00225

query_3_50 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00119'
and unit_id = 44
and metric_type_id in (1,12,17)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00225'
and unit_id = 4
and metric_type_id in (1,12,17)
and %s""")


query_3_51 = ("""select 	'00225' as hcode_id, 'Передержки "окон", продолжительность (час)' as hcode_name, 'час' as hcode_unit_id, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '4' as unit_id, dt, (value/60) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v
where hcode_id = '00119'
and unit_id = 44
and metric_type_id in (1,12,17)
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00225'
and metric_type_id in (1,12,17)
and %s""")

# -- hcode 00306

query_3_72 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00306'
and unit_id = 25
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00328'
and unit_id = 45
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_73 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00306'
and unit_id = 25
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00306' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '25' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00306') hcd
where hcode_id = '00328'
and ind.unit_id = 45
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00308

query_3_74 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00308'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00322'
and unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_75 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00308'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00308' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, '8' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00308') hcd
where hcode_id = '00322'
and ind.unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00309

query_3_76 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00309'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00323'
and unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_77 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00309'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00309' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, '8' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00309') hcd
where hcode_id = '00323'
and ind.unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00310

query_3_78 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00310'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00324'
and unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_79 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00310'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00310' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '17' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00310') hcd
where hcode_id = '00324'
and ind.unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00311

query_3_80 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00311'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00325'
and unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_81 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00311'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00311' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '17' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00311') hcd
where hcode_id = '00325'
and ind.unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00312

query_3_82 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00312'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00326'
and unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_83 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00312'
and unit_id = 17
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00312' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '17' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00312') hcd
where hcode_id = '00326'
and ind.unit_id = 29
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00043

query_3_84 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00043'
and unit_id = 25
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00327'
and unit_id = 45
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_85 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00043'
and unit_id = 25
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00043' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '25' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00043') hcd
where hcode_id = '00327'
and ind.unit_id = 45
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00134

query_3_86 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00134'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00002'
and unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_87 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00134'
and unit_id = 8
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00134' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '8' as unit_id, dt, 
		(value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00134') hcd
where hcode_id = '00002'
and ind.unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- 00334

query_3_88 = ("""select count(0) from dm_rep.dm_all_indicators_v
where calc_rule not in ('influence', 'deviation')
and hcode_id = '00333'
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v 
where calc_rule not in ('influence', 'deviation')
and hcode_id = '00334'
and unit_id = 40
and %s""")

query_3_89 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00334'
and unit_id = 40
and calc_rule not in ('influence', 'deviation')
and %s
except 
select 	'00334' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '40' as unit_id, dt, 
		(value*1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00334') hcd 
where hcode_id = '00333'
and calc_rule not in ('influence', 'deviation')
and %s""")

# -- hcode 00342

query_3_98 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00342'
and unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00155'
and unit_id = 20
and calc_rule not in ('influence', 'deviation')
and %s""")

query_3_99 = ("""select 	hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, 
		unit_id, dt, value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v
where hcode_id = '00342'
and unit_id = 41
and calc_rule not in ('influence', 'deviation')
and %s
except
select 	'00342' as hcode_id, hcd."name", hcd.unit_name, 
		org_id, dor_kod, date_type_id	, metric_type_id, cargo_type_id, val_type_id, '41' as unit_id, dt, 
		(value*1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id 
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm_rep.d_hcode_v where id = '00342') hcd
where hcode_id = '00155'
and ind.unit_id = 20
and calc_rule not in ('influence', 'deviation')
and %s""")



# -- hcode 00361

query_3_100 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00361'
and unit_id = 6
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00358'
and calc_rule not in ('influence', 'deviation')
and %s""")


query_3_101 = ("""select 	'00361' as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '6' as unit_id, dt, (value/1000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm.d_hcode_t where id = '00361') hcd
where hcode_id = '00358'
and calc_rule not in ('influence', 'deviation')
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00361'
and calc_rule not in ('influence', 'deviation')
and %s""")




# -- hcode 00362

query_3_102 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00362'
and unit_id = 6
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00359'
and calc_rule not in ('influence', 'deviation')
and %s""")


query_3_103 = ("""select 	'00362' as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '6' as unit_id, dt, (value/1000000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm.d_hcode_t where id = '00362') hcd
where hcode_id = '00359'
and calc_rule not in ('influence', 'deviation')
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00362'
and calc_rule not in ('influence', 'deviation')
and %s""")



# -- hcode 00363

query_3_104 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00363'
and unit_id = 6
and calc_rule not in ('influence', 'deviation')
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00360'
and calc_rule not in ('influence', 'deviation')
and %s""")


query_3_105 = ("""select 	'00363' as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, org_id, dor_kod, 
		date_type_id, metric_type_id, cargo_type_id, val_type_id, '6' as unit_id, dt, (value/1000000) as value, ss, duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id
	from dm_rep.dm_all_indicators_v ind
	cross join (select * from dm.d_hcode_t where id = '00363') hcd
where hcode_id = '00360'
and calc_rule not in ('influence', 'deviation')
and %s
except
select hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, value, ss, duch_id, nod_id,
		dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00363'
and calc_rule not in ('influence', 'deviation')
and %s""")


# -- hcode '00131'

query_3_29 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00131'
and unit_id = 89
and metric_type_id in (12,2,17,1,10)
and %s
union all
select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00131'
and metric_type_id in (12,2,17,1,10)
and unit_id = 17
and calc_rule = 'ratio'
and %s""")

# QUERYS_3_2 = [v for v in locals() if v.startswith('query')]
#
# QUERYS_3_2_EQUAL = [n for n in QUERYS_3_2 if QUERYS_3_2.index(n) % 2 == 0]
# QUERYS_3_2_EMPTY = [n for n in QUERYS_3_2 if QUERYS_3_2.index(n) % 2 != 0]
#


QUERYS_3_2_EQUAL = ['query_3_25', 'query_3_27', 'query_3_31', 'query_3_32', 'query_3_30', 'query_3_36', 'query_3_38',
                    'query_3_40',
                    'query_3_42', 'query_3_44', 'query_3_46', 'query_3_48', 'query_3_50', 'query_3_72', 'query_3_74',
                    'query_3_76', 'query_3_78', 'query_3_80', 'query_3_82', 'query_3_84', 'query_3_86', 'query_3_88',
                    'query_3_98', 'query_3_100', 'query_3_102', 'query_3_104', 'query_3_29']

QUERYS_3_2_EMPTY = ['query_3_26', 'query_3_28', 'query_3_33', 'query_3_37', 'query_3_39', 'query_3_41', 'query_3_43',
                    'query_3_45', 'query_3_47', 'query_3_49', 'query_3_51', 'query_3_73', 'query_3_75',
                    'query_3_77', 'query_3_79', 'query_3_81', 'query_3_83', 'query_3_85', 'query_3_87', 'query_3_89',
                    'query_3_99', 'query_3_101', 'query_3_103', 'query_3_105']
