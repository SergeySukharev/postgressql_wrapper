
# -- Сравнение всех записей в таблицах
query_2_2_3_4 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, ss varchar, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.val_type_id = 7 and a.date_type_id = 4 and a.metric_type_id in (12,2,18);
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.val_type_id = 7 and a.date_type_id = 4 and a.metric_type_id in (12,2,18);
	return query
select 	a.hcode_id::bpchar, a.hcode_name::varchar(300), a.hcode_unit_name::varchar(30), a.org_id::int8, a.dor_kod::int8, a.date_type_id::int8, 
		a.metric_type_id::int8, a.cargo_type_id::int8, a.val_type_id::int8, a.unit_id::int8, a.dt::date, a.value::float8, a.ss::varchar, 
		a.duch_id::int8, a.nod_id::int8, a.dir_id::int8, a.kato_id::int8, a.vids_id::int8, a.depo_id::int8, a.dep_id::int8
from (select ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 8 as val_type_id, ind.unit_id, dte.dt, (ind.value/dte.month_length*dte.day_of_month 
		+ ind2.value)::numeric(20,6) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
		from public.la_qa1 ind 
		join dm_stg.d_date_t dte
			on 	date_part('month', ind.dt) = date_part('month', dte.dt)
			and date_part('year', ind.dt) = date_part('year', dte.dt)
			and dte.month_from_quater = 2
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on 	ind.hcode_id = hcd.id
			and hcd.group_type = 'базовый'
		left join public.la_qa2 ind2  -- Для пред. месяца
			on (ind.hcode_id = ind2.hcode_id
				and ind.org_id = ind2.org_id
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
				and date_part('month', ind.dt) = (date_part('month', ind2.dt)+1)
				and date_part('year', ind.dt) = date_part('year', ind2.dt))
		--where  dte.dt in ()
		) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select a.hcode_id as hid, a.src, a.priority from dm_lgc.m_hcode_priority_t a) hcp on ind.hcode_id = hcp.hid
		join (select a.hcode_id as hid, a.src, a.priority from dm_lgc.m_hcode_priority_t a where a.src = 'CALC') hcpr on hcp.hid = hcpr.hid
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and ind.metric_type_id in (12,2,18)
	and ind.val_type_id = 8
	and ind.date_type_id = 3
	and hcd.group_type in ('базовый')) b
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
    and a.%s
   ;
end;
$f$
;""")

query_2_2_3_5 = ("""select clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
		from dm_rep.dm_all_indicators_v clc
		join dm_stg.d_date_t dte
			on dte.dt = clc.dt
		join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'базовый'
	and metric_type_id in (12,2,18)
	and val_type_id = 8
	and date_type_id = 3
	and dte.month_from_quater = 2
	and clc.%s
except
select * from public.lilo_auto_qa()""")



# -- Сравнение всех записей в таблицах
query_2_2_3_7 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, ss varchar, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.val_type_id = 7 and a.date_type_id = 4 and a.metric_type_id in (12,2,18);
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.val_type_id = 7 and a.date_type_id = 4 and a.metric_type_id in (12,2,18);
	create table public.la_qa3 as 
		select * from dm_rep.dm_all_indicators_v a where a.val_type_id = 7 and a.date_type_id = 4 and a.metric_type_id in (12,2,18);
	return query
select 	a.hcode_id::bpchar, a.hcode_name::varchar(300), a.hcode_unit_name::varchar(30), a.org_id::int8, a.dor_kod::int8, a.date_type_id::int8, 
		a.metric_type_id::int8, a.cargo_type_id::int8, a.val_type_id::int8, a.unit_id::int8, a.dt::date, a.value::float8, a.ss::varchar, 
		a.duch_id::int8, a.nod_id::int8, a.dir_id::int8, a.vids_id::int8, a.kato_id::int8, a.depo_id::int8, a.dep_id::int8
from (select 	ind.hcode_id, ind.hcode_name, ind.hcode_unit_name, ind.org_id, ind.dor_kod, 3 as date_type_id, ind.metric_type_id, 
		ind.cargo_type_id, 8 as val_type_id, ind.unit_id, dte.dt, (ind.value/dte.month_length*dte.day_of_month 
		+ ind2.value + ind3.value)::numeric(20,6) as value, ind.ss, ind.duch_id, ind.nod_id, ind.dir_id, ind.vids_id, ind.kato_id, ind.depo_id, ind.dep_id
	from public.la_qa1 ind 
	join dm_stg.d_date_t dte
		on 	date_part('month', ind.dt) = date_part('month', dte.dt)
		and date_part('year', ind.dt) = date_part('year', dte.dt)
		and dte.month_from_quater = 3
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on 	ind.hcode_id = hcd.id
		and hcd.group_type = 'базовый'
	left join public.la_qa2 ind2  -- пред. месяц квартала
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
	left join public.la_qa3 ind3   -- первый месяц квартала
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
			and ind.dir_id = ind3.dir_id 
			and ind3.val_type_id = 7
			and ind3.date_type_id = 4
			and date_part('month', ind.dt) = (date_part('month', ind3.dt)+2)
			and date_part('year', ind.dt) = date_part('year', ind3.dt))
	--where dte.dt in ()
	) a
left join ( -- Секция выявления более приоритетных дублей
	select  *
		from dm_stg.calc_src_indicators_t ind 
		join (select a.hcode_id as hid, a.src, a.priority from dm_lgc.m_hcode_priority_t a) hcp on ind.hcode_id = hcp.hid
		join (select a.hcode_id as hid, a.src, a.priority from dm_lgc.m_hcode_priority_t a where a.src = 'CALC') hcpr on hcp.hid = hcpr.hid
		left join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
			on ind.hcode_id = hcd.id
	where hcp.priority < hcpr.priority -- Отбор записей с большим приоритетом
	and ind.metric_type_id in (12,2,18)
	and ind.val_type_id = 8
	and ind.date_type_id = 3
	and hcd.group_type in ('базовый')) b
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
    and a.%s
    ;
end;
$f$
;""")


query_2_2_3_8 = ("""select * from public.lilo_auto_qa()
except
select 	clc.hcode_id, clc.hcode_name, clc.hcode_unit_name, clc.org_id, clc.dor_kod, clc.date_type_id, clc.metric_type_id, clc.cargo_type_id, 
		clc.val_type_id, clc.unit_id, clc.dt::date, clc.value::numeric(20,6), clc.ss, clc.duch_id, clc.nod_id, clc.dir_id, clc.vids_id, clc.kato_id, clc.depo_id, clc.dep_id
	from dm_rep.dm_all_indicators_v clc
	join dm_stg.d_date_t dte
		on dte.dt = clc.dt
	join (select distinct id, group_type from dm_stg.d_hcode_t) hcd
		on hcd.id = clc.hcode_id
where 	calc_rule = 'growplan'
	and hcd.group_type = 'базовый'
	and metric_type_id in (12,2,18)
	and val_type_id = 8
	and date_type_id = 3
	and dte.month_from_quater = 3
	and clc.%s""")

QUERYS_2_3_3 = [('query_2_2_3_4', 'query_2_2_3_5'), ('query_2_2_3_7', 'query_2_2_3_8')]
