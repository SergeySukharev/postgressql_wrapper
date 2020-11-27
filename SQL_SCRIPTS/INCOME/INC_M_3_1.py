# ----------------------------------
# ---- 3.1 Расчетные показатели ----
# ----------------------------------

# -- hcode '00004'

# -- Сравнение кол-ва записей

query_3_01 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00327') and unit_id = 45 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00131') and unit_id in (17,89) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_02 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00004'
and calc_rule = 'income'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Ожидаемый результат: Кол-во записей должно совпадать.


# -- Полная сверка
query_3_03 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00327') and a.unit_id = 45 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00131') and a.unit_id in (17,89) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00004'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	49::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/b.value)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00004') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_04 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00004'
and calc_rule = 'income'
and %s
""")

# -- Ожидаемый результат: Запрос должен возвращать пустой вывод.



# -- hcode '00065'
query_3_05 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00097')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00081') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_06 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00065'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")



query_3_07 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00097') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00081') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00065'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00065') hcd
    where a.%s
    ;
end;
$f$
;""")



query_3_08 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00065'
and calc_rule = 'ratio'
and %s
""")


# -- hcode '00066'

query_3_09 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00081')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00069') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_010 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00066'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

query_3_011 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00081') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00069') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00066'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00066') hcd
    where a.%s
    ;
end;
$f$
;""")


query_3_012 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00066'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00067'

query_3_013 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00097')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00069') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_014 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00067'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка
 
query_3_015 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00097') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00069') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00067'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00067') hcd
    where a.%s
    ;
end;
$f$
;""")


query_3_016 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00067'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00099'
query_3_017 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00100')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00105') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_018 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00099'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_019 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00100') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00105') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00099'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00099') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_020 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00099'
and calc_rule = 'ratio'
and %s""")



# -- hcode '00103'

query_3_021 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00100')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00102') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_022 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00103'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка

query_3_023 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00100') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00102') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00103'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00103') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_024 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00103'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00104'

query_3_025 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00105')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00102') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_026 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00104'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_027 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00105') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00102') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00104'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	22::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00104') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_028 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00104'
and calc_rule = 'ratio'
and %s""")



# -- hcode '00031'

query_3_029 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00011')and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00028') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_030 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00031'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_031 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00011') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00028') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00031'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	39::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0))::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00031') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_032 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00031'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00149' - закомментировано



# -- hcode '00150'

query_3_033 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00018') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_034 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00150'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_035 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00018') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00150'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/nullif(b.value,0))*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00150') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_036 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00150'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00151'

query_3_037 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00019') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_038 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00151'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка
 
query_3_039 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00019') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00151'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/nullif(b.value,0))*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00151') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_040 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00151'
and calc_rule = 'ratio'
and %s""")


# -- hcode '00152'

query_3_041 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00020') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_042 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00152'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка
 
query_3_043 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00020') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00152'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/nullif(b.value,0))*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00152') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_044 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00152'
and calc_rule = 'ratio'
and %s
""")



# -- hcode 00216

query_3_045 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from (
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id
    where ab.%s
	;
end;
$f$
;""")

query_3_046 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00216'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


query_3_047 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.calc_rule not in ('influence', 'deviation');	 
	return query
select 
	'00216'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (ab.org_id, c.org_id)::int8 as org_id,  
	coalesce (ab.dor_kod, c.dor_kod)::int8 as dor_kod,  
	coalesce (ab.date_type_id, c.date_type_id)::int8 as date_type_id, 
	coalesce (ab.metric_type_id, c.metric_type_id)::int8 as metric_type_id, 
	coalesce (ab.cargo_type_id, c.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (ab.val_type_id, c.val_type_id)::int8 as val_type_id, 
  	48::int8 as unit_id, 
 	coalesce (ab.dt, c.dt)::date as dt, 
  	(((ab.value+c.value)/60)::numeric(20,6))::float8 as value, 
	coalesce (ab.duch_id, c.duch_id)::int8 as duch_id, 
	coalesce (ab.nod_id, c.nod_id)::int8 as nod_id, 
	coalesce (ab.dir_id, c.dir_id)::int8 as dir_id, 
	coalesce (ab.kato_id, c.kato_id)::int8 as kato_id, 
	coalesce (ab.vids_id, c.vids_id)::int8 as vids_id,
	coalesce (ab.depo_id, c.depo_id)::int8 as depo_id,
	coalesce (ab.dep_id, c.dep_id)::int8 as dep_id
from (
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value+b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id
cross join (select * from dm.d_hcode_t where id = '00216') hcd
    where ab.%s
    ;
end;
$f$
;""")

query_3_048 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00216'
and calc_rule = 'ratio'
and %s
""")



# hcode 00115

query_3_073 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00132') and unit_id = 41 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00002') and unit_id = 41 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_074 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00115'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_075 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00132') and a.unit_id = 41 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00002') and a.unit_id = 41 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00115'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	46::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/b.value)*100-100)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00115') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_076 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00115'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00297


query_3_077 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00109') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_078 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00297'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка

query_3_079 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00109') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00297'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00297') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_080 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00297'
and calc_rule = 'ratio'
and %s
""")



# --hcode 00298

query_3_049 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	create table public.la_qa1 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id = 1; 
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17; 
	return query
select count(0) from (
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	left join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id
    where abc.%s
    ;
end;
$f$
;""")

query_3_050 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00298'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

query_3_051 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	create table public.la_qa1 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.metric_type_id = 1; 
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17; 
	return query
select '00298'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abc.org_id, abc.dor_kod, 
  		abc.date_type_id, abc.metric_type_id, abc.cargo_type_id, abc.val_type_id, 138::int8 as unit_id, abc.dt, 
  		((((abc.value/60)/nullif(d.value,0))*1000000)::numeric(20,6))::float8 as value, 
  		abc.duch_id, abc.nod_id, abc.dir_id, abc.kato_id, abc.vids_id,abc.depo_id, abc.dep_id
from ( 
select  
coalesce (ab.org_id, c.org_id)::int8 as org_id,  
coalesce (ab.dor_kod, c.dor_kod)::int8 as dor_kod,  
coalesce (ab.date_type_id, c.date_type_id)::int8 as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id)::int8 as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id)::int8 as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id)::int8 as val_type_id, 
coalesce (ab.dt, c.dt)::date as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id)::int8 as duch_id, 
coalesce (ab.nod_id, c.nod_id)::int8 as nod_id, 
coalesce (ab.dir_id, c.dir_id)::int8 as dir_id, 
coalesce (ab.kato_id, c.kato_id)::int8 as kato_id, 
coalesce (ab.vids_id, c.vids_id)::int8 as vids_id,
coalesce (ab.depo_id, c.depo_id)::int8 as depo_id,
coalesce (ab.dep_id, c.dep_id)::int8 as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value+b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	left join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id
cross join (select * from dm.d_hcode_t where id = '00298') hcd
    where abc.%s
    ;
end;
$f$
;""")

query_3_052 = ("""select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00298'
and calc_rule = 'ratio'
and %s
except
select * from public.lilo_auto_qa()""")


# --hcode 00299


query_3_081 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00111') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_082 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00299'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_083 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00111') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00299'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00299') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_084 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00299'
and calc_rule = 'ratio'
and %s""")



# --hcode 00300


query_3_085 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00165') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_086 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00300'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_087 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00165') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00300'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00300') hcd
where a.%s
    ;
end;
$f$
;""")

query_3_088 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00300'
and calc_rule = 'ratio'
and %s""")


# --hcode 00301


query_3_089 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00166') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_090 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00301'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_091 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00166') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00301'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00301') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_092 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00301'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00302


query_3_093 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00167') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_094 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00302'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_095 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00167') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00302'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00302') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_096 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00302'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00303


query_3_097 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_098 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00303'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_099 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00303'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00303') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0100 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00303'
and calc_rule = 'ratio'
and %s""")


# --hcode 00304

query_3_0101 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0102 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00304'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_0103 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00304'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00304') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0104 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00304'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00305

query_3_0105 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id = 1 and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17 and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0106 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00305'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_0107 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.metric_type_id = 1 and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17 and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00305'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	138::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/60/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00305') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0108 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00305'
and calc_rule = 'ratio'
and %s
""")



# --hcode 00317

query_3_053 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	create table public.la_qa1 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id = 1; 
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17; 
	return query
select count(0) from (
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	left join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
    where abc.%s
    ;
end;
$f$
;""")

query_3_054 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00298'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

query_3_055 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	create table public.la_qa1 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.metric_type_id = 1; 
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17; 
	return query
select '00298'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abc.org_id, abc.dor_kod, 
  		abc.date_type_id, abc.metric_type_id, abc.cargo_type_id, abc.val_type_id, 138::int8 as unit_id, abc.dt, 
  		((((abc.value/60)/nullif(d.value,0))*1000000)::numeric(20,6))::float8 as value, 
  		abc.duch_id, abc.nod_id, abc.dir_id, abc.kato_id, abc.vids_id, abc.depo_id, abc.dep_id
from ( 
select  
coalesce (ab.org_id, c.org_id)::int8 as org_id,  
coalesce (ab.dor_kod, c.dor_kod)::int8 as dor_kod,  
coalesce (ab.date_type_id, c.date_type_id)::int8 as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id)::int8 as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id)::int8 as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id)::int8 as val_type_id, 
coalesce (ab.dt, c.dt)::date as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id)::int8 as duch_id, 
coalesce (ab.nod_id, c.nod_id)::int8 as nod_id, 
coalesce (ab.dir_id, c.dir_id)::int8 as dir_id, 
coalesce (ab.kato_id, c.kato_id)::int8 as kato_id, 
coalesce (ab.vids_id, c.vids_id)::int8 as vids_id,
coalesce (ab.depo_id, c.depo_id)::int8 as depo_id,
coalesce (ab.dep_id, c.dep_id)::int8 as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value+b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	left join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id
cross join (select * from dm.d_hcode_t where id = '00298') hcd
    where abc.%s
    ;
end;
$f$
;""")

query_3_056 = ("""select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00298'
and calc_rule = 'ratio'
and %s
except
select * from public.lilo_auto_qa()""")


# --hcode 00335

query_3_0109 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00318') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0110 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00335'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 

query_3_0111 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00318') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00335'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00335') hcd
    where a.%s
    ;
end;
$f$
;""")


query_3_0112 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00335'
and calc_rule = 'ratio'
and %s
""") 
      
      
# --hcode 00336

query_3_0113 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00319') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0114 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00336'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка

query_3_0115 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00319') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00336'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00336') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0116 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00336'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00337

query_3_0117 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00320') and metric_type_id in (1) and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id in (17) and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0118 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00337'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_0119 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00320') and a.metric_type_id in (1) and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id in (17) and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00337'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	1::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	106::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	(((a.value/b.value)*1000000)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00337') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0120 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00337'
and calc_rule = 'ratio'
and %s
""")



# -- hcode '00341'

# -- Сравнение кол-ва записей

query_3_057 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	drop table if exists public.la_qa6;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00109') and metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00111') and metric_type_id = 1;
	create table public.la_qa3 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id = 1;
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id = 1;
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id = 1; 
	create table public.la_qa6 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17; 
	return query
select count(0) from (
select  
coalesce (abcd.org_id, e.org_id) as org_id,  
coalesce (abcd.date_type_id, e.date_type_id) as date_type_id, 
coalesce (abcd.metric_type_id, e.metric_type_id) as metric_type_id, 
coalesce (abcd.cargo_type_id, e.cargo_type_id) as cargo_type_id, 
coalesce (abcd.val_type_id, e.val_type_id) as val_type_id, 
coalesce (abcd.dt, e.dt) as dt, 
coalesce (abcd.duch_id, e.duch_id) as duch_id, 
coalesce (abcd.nod_id, e.nod_id) as nod_id, 
coalesce (abcd.dir_id, e.dir_id) as dir_id, 
coalesce (abcd.kato_id, e.kato_id) as kato_id, 
coalesce (abcd.vids_id, e.vids_id) as vids_id,
coalesce (abcd.depo_id, e.depo_id) as depo_id,
coalesce (abcd.dep_id, e.dep_id) as dep_id
from(
select  
coalesce (abc.org_id, d.org_id) as org_id,  
coalesce (abc.date_type_id, d.date_type_id) as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id) as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id) as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id) as val_type_id, 
coalesce (abc.dt, d.dt) as dt, 
coalesce (abc.duch_id, d.duch_id) as duch_id, 
coalesce (abc.nod_id, d.nod_id) as nod_id, 
coalesce (abc.dir_id, d.dir_id) as dir_id, 
coalesce (abc.kato_id, d.kato_id) as kato_id, 
coalesce (abc.vids_id, d.vids_id) as vids_id,
coalesce (abc.depo_id, d.depo_id) as depo_id,
coalesce (abc.dep_id, d.dep_id) as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id)abcd
	full join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id)abcde
	join public.la_qa6 f
		on 	abcde.org_id = f.org_id
		and abcde.date_type_id = f.date_type_id
		and abcde.cargo_type_id = f.cargo_type_id
		and abcde.val_type_id = f.val_type_id
		and abcde.dt = f.dt
		and abcde.nod_id = f.nod_id
		and abcde.duch_id = f.duch_id
		and abcde.vids_id = f.vids_id 
		and abcde.kato_id = f.kato_id 
		and abcde.dir_id = f.dir_id
		and abcde.depo_id = f.depo_id
		and abcde.dep_id = f.dep_id
    where abcde.%s
    ;
end;
$f$
;""")


query_3_058 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00341'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Ожидаемый результат: Кол-во записей должно совпадать.


# -- Полная сверка
query_3_059 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	drop table if exists public.la_qa6;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00109') and a.metric_type_id = 1;
	create table public.la_qa2 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00111') and a.metric_type_id = 1;
	create table public.la_qa3 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.metric_type_id = 1;
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.metric_type_id = 1;
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.metric_type_id = 1; 
	create table public.la_qa6 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17; 
	return query
select '00341'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abcde.org_id, abcde.dor_kod, 
  		abcde.date_type_id, abcde.metric_type_id, abcde.cargo_type_id, abcde.val_type_id, 138::int8 as unit_id, abcde.dt, 
  		((((abcde.value/60)/nullif(f.value,0))*1000000)::numeric(20,6))::float8 as value, 
  		abcde.duch_id, abcde.nod_id, abcde.dir_id, abcde.kato_id, abcde.vids_id, abcde.depo_id, abcde.dep_id
from ( 
select  
coalesce (abcd.org_id, e.org_id)::int8 as org_id,  
coalesce (abcd.dor_kod, e.dor_kod)::int8 as dor_kod,  
coalesce (abcd.date_type_id, e.date_type_id)::int8 as date_type_id, 
coalesce (abcd.metric_type_id, e.metric_type_id)::int8 as metric_type_id, 
coalesce (abcd.cargo_type_id, e.cargo_type_id)::int8 as cargo_type_id, 
coalesce (abcd.val_type_id, e.val_type_id)::int8 as val_type_id, 
coalesce (abcd.dt, e.dt)::date as dt, 
(abcd.value+e.value)::float8 as value,
coalesce (abcd.duch_id, e.duch_id)::int8 as duch_id, 
coalesce (abcd.nod_id, e.nod_id)::int8 as nod_id, 
coalesce (abcd.dir_id, e.dir_id)::int8 as dir_id, 
coalesce (abcd.kato_id, e.kato_id)::int8 as kato_id, 
coalesce (abcd.vids_id, e.vids_id)::int8 as vids_id,
coalesce (abcd.depo_id, e.depo_id)::int8 as depo_id,
coalesce (abcd.dep_id, e.dep_id)::int8 as dep_id
from(
select  
coalesce (abc.org_id, d.org_id) as org_id,
coalesce (abc.dor_kod, d.dor_kod) as dor_kod,
coalesce (abc.date_type_id, d.date_type_id) as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id) as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id) as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id) as val_type_id, 
coalesce (abc.dt, d.dt) as dt, 
(abc.value+d.value)::float8 as value,
coalesce (abc.duch_id, d.duch_id) as duch_id, 
coalesce (abc.nod_id, d.nod_id) as nod_id, 
coalesce (abc.dir_id, d.dir_id) as dir_id, 
coalesce (abc.kato_id, d.kato_id) as kato_id, 
coalesce (abc.vids_id, d.vids_id) as vids_id,
coalesce (abc.depo_id, d.depo_id) as depo_id,
coalesce (abc.dep_id, d.dep_id) as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,
coalesce (ab.dor_kod, c.dor_kod) as dor_kod,
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value+b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
 full join public.la_qa2 b
		on 	a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on 	ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id) abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id) abcd
	full join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id) abcde
	join public.la_qa6 f
		on 	abcde.org_id = f.org_id
		and abcde.date_type_id = f.date_type_id
		and abcde.cargo_type_id = f.cargo_type_id
		and abcde.val_type_id = f.val_type_id
		and abcde.dt = f.dt
		and abcde.nod_id = f.nod_id
		and abcde.duch_id = f.duch_id
		and abcde.vids_id = f.vids_id 
		and abcde.kato_id = f.kato_id 
		and abcde.dir_id = f.dir_id
		and abcde.depo_id = f.depo_id
		and abcde.dep_id = f.dep_id
cross join (select * from dm.d_hcode_t where id = '00341') hcd
    where abcde.%s
    ;
end;
$f$
;""")

query_3_060 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00341'
and calc_rule = 'ratio'
and %s
""")

# -- Ожидаемый результат: Запрос должен возвращать пустой вывод.



# -- hcode '00340'

query_3_061 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00109') and metric_type_id = 1;
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00168') and metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00169') and metric_type_id = 1;
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00170') and metric_type_id = 1; 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00154') and metric_type_id = 17; 
	return query
select count(0) from (
select  
coalesce (abc.org_id, d.org_id) as org_id,  
coalesce (abc.date_type_id, d.date_type_id) as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id) as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id) as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id) as val_type_id, 
coalesce (abc.dt, d.dt) as dt, 
coalesce (abc.duch_id, d.duch_id) as duch_id, 
coalesce (abc.nod_id, d.nod_id) as nod_id, 
coalesce (abc.dir_id, d.dir_id) as dir_id, 
coalesce (abc.kato_id, d.kato_id) as kato_id, 
coalesce (abc.vids_id, d.vids_id) as vids_id,
coalesce (abc.depo_id, d.depo_id) as depo_id,
coalesce (abc.dep_id, d.dep_id) as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
    full join public.la_qa2 b
        on  a.org_id = b.org_id
        and a.date_type_id = b.date_type_id
        and a.cargo_type_id = b.cargo_type_id
        and a.val_type_id = b.val_type_id
        and a.dt = b.dt
        and a.nod_id = b.nod_id
        and a.duch_id = b.duch_id
        and a.vids_id = b.vids_id 
        and a.kato_id = b.kato_id 
        and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
   full join public.la_qa3 c
        on  ab.org_id = c.org_id
        and ab.date_type_id = c.date_type_id
        and ab.cargo_type_id = c.cargo_type_id
        and ab.val_type_id = c.val_type_id
        and ab.dt = c.dt
      and ab.nod_id = c.nod_id
      and ab.duch_id = c.duch_id
      and ab.vids_id = c.vids_id 
      and ab.kato_id = c.kato_id 
      and ab.dir_id = c.dir_id
	  and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
     on abc.org_id = d.org_id
      and abc.date_type_id = d.date_type_id
      and abc.cargo_type_id = d.cargo_type_id
      and abc.val_type_id = d.val_type_id
      and abc.dt = d.dt
      and abc.nod_id = d.nod_id
      and abc.duch_id = d.duch_id
      and abc.vids_id = d.vids_id 
      and abc.kato_id = d.kato_id 
      and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id
     )abcd
 join public.la_qa5 e
     on abcd.org_id = e.org_id
      and abcd.date_type_id = e.date_type_id
      and abcd.cargo_type_id = e.cargo_type_id
      and abcd.val_type_id = e.val_type_id
      and abcd.dt = e.dt
      and abcd.nod_id = e.nod_id
      and abcd.duch_id = e.duch_id
      and abcd.vids_id = e.vids_id 
      and abcd.kato_id = e.kato_id 
      and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
    where abcd.%s
    ;
end;
$f$
;""")

query_3_062 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00340'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


query_3_063 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00109') and a.metric_type_id = 1;
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00168') and a.metric_type_id = 1;
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00169') and a.metric_type_id = 1;
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00170') and a.metric_type_id = 1; 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00154') and a.metric_type_id = 17; 
	return query
select '00340'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abcd.org_id, abcd.dor_kod, 
  		abcd.date_type_id, abcd.metric_type_id, abcd.cargo_type_id, abcd.val_type_id, 138::int8 as unit_id, abcd.dt, 
  		((((abcd.value/60)/nullif(e.value,0))*1000000)::numeric(20,6))::float8 as value, 
  		abcd.duch_id, abcd.nod_id, abcd.dir_id, abcd.kato_id, abcd.vids_id, abcd.depo_id, abcd.dep_id
from ( 
select  
coalesce (abc.org_id, d.org_id)::int8 as org_id,  
coalesce (abc.dor_kod, d.dor_kod)::int8 as dor_kod,  
coalesce (abc.date_type_id, d.date_type_id)::int8 as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id)::int8 as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id)::int8 as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id)::int8 as val_type_id, 
coalesce (abc.dt, d.dt)::date as dt, 
(abc.value+d.value)::float8 as value,
coalesce (abc.duch_id, d.duch_id)::int8 as duch_id, 
coalesce (abc.nod_id, d.nod_id)::int8 as nod_id, 
coalesce (abc.dir_id, d.dir_id)::int8 as dir_id, 
coalesce (abc.kato_id, d.kato_id)::int8 as kato_id, 
coalesce (abc.vids_id, d.vids_id)::int8 as vids_id,
coalesce (abc.depo_id, d.depo_id)::int8 as depo_id,
coalesce (abc.dep_id, d.dep_id)::int8 as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,
coalesce (ab.dor_kod, c.dor_kod) as dor_kod,
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value+b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
 full join public.la_qa2 b
     on a.org_id = b.org_id
      and a.date_type_id = b.date_type_id
      and a.cargo_type_id = b.cargo_type_id
      and a.val_type_id = b.val_type_id
      and a.dt = b.dt
      and a.nod_id = b.nod_id
      and a.duch_id = b.duch_id
      and a.vids_id = b.vids_id 
      and a.kato_id = b.kato_id 
      and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
   full join public.la_qa3 c
     on ab.org_id = c.org_id
      and ab.date_type_id = c.date_type_id
      and ab.cargo_type_id = c.cargo_type_id
      and ab.val_type_id = c.val_type_id
      and ab.dt = c.dt
      and ab.nod_id = c.nod_id
      and ab.duch_id = c.duch_id
      and ab.vids_id = c.vids_id 
      and ab.kato_id = c.kato_id 
      and ab.dir_id = c.dir_id
	  and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
     on abc.org_id = d.org_id
      and abc.date_type_id = d.date_type_id
      and abc.cargo_type_id = d.cargo_type_id
      and abc.val_type_id = d.val_type_id
      and abc.dt = d.dt
      and abc.nod_id = d.nod_id
      and abc.duch_id = d.duch_id
      and abc.vids_id = d.vids_id 
      and abc.kato_id = d.kato_id 
      and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id
     )abcd
 join public.la_qa5 e
     on abcd.org_id = e.org_id
      and abcd.date_type_id = e.date_type_id
      and abcd.cargo_type_id = e.cargo_type_id
      and abcd.val_type_id = e.val_type_id
      and abcd.dt = e.dt
      and abcd.nod_id = e.nod_id
      and abcd.duch_id = e.duch_id
      and abcd.vids_id = e.vids_id 
      and abcd.kato_id = e.kato_id 
      and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
cross join (select * from dm.d_hcode_t where id = '00340') hcd
    where abcd.%s
    ;
end;
$f$
;""")

query_3_064 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00340'
and calc_rule = 'ratio'
and %s
""")


# hcode 00073

query_3_065 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00074') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00075') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$""")

query_3_066 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00073'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

query_3_067 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00074') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00075') and a.calc_rule not in ('influence', 'deviation'); 
	return query
select 
	'00073'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	6::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value+b.value)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00073') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_068 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00073'
and calc_rule = 'ratio'
and %s
""")



# hcode 00003

query_3_069 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00077') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00078') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_070 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00003'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

query_3_071 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00077') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00078') and a.calc_rule not in ('influence', 'deviation'); 
	return query
select 
	'00003'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	37::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value+b.value)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00003') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_072 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00003'
and calc_rule = 'ratio'
and %s
""")

# hcode = 00339


query_3_0121 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00112') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00021') and calc_rule not in ('influence', 'deviation');
	return query
select count(0) from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id 
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
    where a.%s
	;
end;
$f$
;""")

query_3_0122 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00339'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")


# -- Полная сверка

query_3_0123 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00112') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00021') and a.calc_rule not in ('influence', 'deviation');
	return query
select 
	'00339'::bpchar as hcode_id, 
	hcd.name as hcode_name, 
	hcd.unit_name as hcode_unit_name, 
	coalesce (a.org_id, b.org_id)::int8 as org_id,  
	coalesce (a.dor_kod, b.dor_kod)::int8 as dor_kod,  
	coalesce (a.date_type_id, b.date_type_id)::int8 as date_type_id, 
	coalesce (a.metric_type_id, b.metric_type_id)::int8 as metric_type_id, 
	coalesce (a.cargo_type_id, b.cargo_type_id)::int8 as cargo_type_id, 
	coalesce (a.val_type_id, b.val_type_id)::int8 as val_type_id, 
  	4::int8 as unit_id, 
 	coalesce (a.dt, b.dt)::date as dt, 
  	((a.value/nullif(b.value,0)/60)::numeric(20,6))::float8 as value, 
	coalesce (a.duch_id, b.duch_id)::int8 as duch_id, 
	coalesce (a.nod_id, b.nod_id)::int8 as nod_id, 
	coalesce (a.dir_id, b.dir_id)::int8 as dir_id, 
	coalesce (a.kato_id, b.kato_id)::int8 as kato_id, 
	coalesce (a.vids_id, b.vids_id)::int8 as vids_id,
coalesce (a.depo_id, b.depo_id)::int8 as depo_id,
coalesce (a.dep_id, b.dep_id)::int8 as dep_id
from public.la_qa1 a
	left join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id
cross join (select * from dm.d_hcode_t where id = '00339') hcd
    where a.%s
    ;
end;
$f$
;""")

query_3_0124 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00339'
and calc_rule = 'ratio'
and %s
""")


# --hcode 00049

query_3_0125 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00064') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00063') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00329') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00330') and calc_rule not in ('influence', 'deviation'); 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00064') and calc_rule not in ('influence', 'deviation'); 
	return query
select count(0) from (
select  
coalesce (abc.org_id, d.org_id) as org_id,  
coalesce (abc.date_type_id, d.date_type_id) as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id) as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id) as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id) as val_type_id, 
coalesce (abc.dt, d.dt) as dt, 
coalesce (abc.duch_id, d.duch_id) as duch_id, 
coalesce (abc.nod_id, d.nod_id) as nod_id, 
coalesce (abc.dir_id, d.dir_id) as dir_id, 
coalesce (abc.kato_id, d.kato_id) as kato_id, 
coalesce (abc.vids_id, d.vids_id) as vids_id,
coalesce (abc.depo_id, d.depo_id) as depo_id,
coalesce (abc.dep_id, d.dep_id) as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.metric_type_id = d.metric_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id)abcd
	left join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.metric_type_id = e.metric_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
    where abcd.%s
    ;
end;
$f$
;""")

query_3_0126 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00049'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_0127 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00064') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00063') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00329') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00330') and a.calc_rule not in ('influence', 'deviation'); 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00064') and a.calc_rule not in ('influence', 'deviation'); 	 
	return query
select '00049'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abcd.org_id, abcd.dor_kod, 
  		abcd.date_type_id, abcd.metric_type_id, abcd.cargo_type_id, abcd.val_type_id, 46::int8 as unit_id, abcd.dt, 
  		(((abcd.value/nullif(e.value,0))*100)::numeric(20,6))::float8 as value, abcd.duch_id, abcd.nod_id, abcd.dir_id, abcd.kato_id, abcd.vids_id, abcd.depo_id, abcd.dep_id
from ( 
select  
coalesce (abc.org_id, d.org_id)::int8 as org_id,  
coalesce (abc.dor_kod, d.dor_kod)::int8 as dor_kod,  
coalesce (abc.date_type_id, d.date_type_id)::int8 as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id)::int8 as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id)::int8 as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id)::int8 as val_type_id, 
coalesce (abc.dt, d.dt)::date as dt, 
(abc.value-d.value)::float8 as value,
coalesce (abc.duch_id, d.duch_id)::int8 as duch_id, 
coalesce (abc.nod_id, d.nod_id)::int8 as nod_id, 
coalesce (abc.dir_id, d.dir_id)::int8 as dir_id, 
coalesce (abc.kato_id, d.kato_id)::int8 as kato_id, 
coalesce (abc.vids_id, d.vids_id)::int8 as vids_id,
coalesce (abc.depo_id, d.depo_id)::int8 as depo_id,
coalesce (abc.dep_id, d.dep_id)::int8 as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,
coalesce (ab.dor_kod, c.dor_kod) as dor_kod,
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value-b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id, 
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.metric_type_id = d.metric_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id)abcd
	left join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.metric_type_id = e.metric_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
cross join (select * from dm.d_hcode_t where id = '00049') hcd
    where abcd.%s
    ;
end;
$f$
;""")

query_3_0128 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00049'
and calc_rule = 'ratio'
and %s""")


# --hcode 00053

query_3_0129 = ("""create or replace function public.lilo_auto_qa() returns table(cnt int8)
language plpgsql
as $f$
begin
	drop table if exists public.la_qa1;
	drop table if exists public.la_qa2;
	drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00072') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00071') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00331') and calc_rule not in ('influence', 'deviation');
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00332') and calc_rule not in ('influence', 'deviation'); 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v where hcode_id in ('00072') and calc_rule not in ('influence', 'deviation'); 
	return query
select count(0) from (
select  
coalesce (abc.org_id, d.org_id) as org_id,  
coalesce (abc.date_type_id, d.date_type_id) as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id) as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id) as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id) as val_type_id, 
coalesce (abc.dt, d.dt) as dt, 
coalesce (abc.duch_id, d.duch_id) as duch_id, 
coalesce (abc.nod_id, d.nod_id) as nod_id, 
coalesce (abc.dir_id, d.dir_id) as dir_id, 
coalesce (abc.kato_id, d.kato_id) as kato_id, 
coalesce (abc.vids_id, d.vids_id) as vids_id,
coalesce (abc.depo_id, d.depo_id) as depo_id,
coalesce (abc.dep_id, d.dep_id) as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,  
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.metric_type_id = d.metric_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id)abcd
	left join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.metric_type_id = e.metric_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
    where abcd.%s
    ;
end;
$f$
;""")

query_3_0130 = ("""select count(0) from dm_rep.dm_all_indicators_v
where hcode_id = '00053'
and calc_rule = 'ratio'
and %s
union all
select * from public.lilo_auto_qa();""")

# -- Полная сверка
 
query_3_0131 = ("""create or replace function public.lilo_auto_qa() 
	returns table(	hcode_id bpchar, hcode_name varchar(300), hcode_unit_name varchar(30), org_id int8, dor_kod int8, 
					date_type_id int8, metric_type_id int8, cargo_type_id int8, val_type_id int8, unit_id int8, dt date, 
					value float8, duch_id int8, nod_id int8, dir_id int8, kato_id int8, vids_id int8, depo_id int8, dep_id int8)
language plpgsql
as $f$
begin
    drop table if exists public.la_qa1;
    drop table if exists public.la_qa2;
    drop table if exists public.la_qa3;
	drop table if exists public.la_qa4;
	drop table if exists public.la_qa5;
	create table public.la_qa1 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00072') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa2 as 
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00071') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa3 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00331') and a.calc_rule not in ('influence', 'deviation');
	create table public.la_qa4 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00332') and a.calc_rule not in ('influence', 'deviation'); 
	create table public.la_qa5 as
		select * from dm_rep.dm_all_indicators_v a where a.hcode_id in ('00072') and a.calc_rule not in ('influence', 'deviation'); 	 
	return query
select '00053'::bpchar as hcode_id, hcd.name as hcode_name, hcd.unit_name as hcode_unit_name, abcd.org_id, abcd.dor_kod, 
  		abcd.date_type_id, abcd.metric_type_id, abcd.cargo_type_id, abcd.val_type_id, 46::int8 as unit_id, abcd.dt, 
  		(((abcd.value/e.value)*100)::numeric(20,6))::float8 as value, abcd.duch_id, abcd.nod_id, abcd.dir_id, abcd.kato_id, abcd.vids_id, abcd.depo_id, abcd.dep_id
from ( 
select  
coalesce (abc.org_id, d.org_id)::int8 as org_id,  
coalesce (abc.dor_kod, d.dor_kod)::int8 as dor_kod,  
coalesce (abc.date_type_id, d.date_type_id)::int8 as date_type_id, 
coalesce (abc.metric_type_id, d.metric_type_id)::int8 as metric_type_id, 
coalesce (abc.cargo_type_id, d.cargo_type_id)::int8 as cargo_type_id, 
coalesce (abc.val_type_id, d.val_type_id)::int8 as val_type_id, 
coalesce (abc.dt, d.dt)::date as dt, 
(abc.value-d.value)::float8 as value,
coalesce (abc.duch_id, d.duch_id)::int8 as duch_id, 
coalesce (abc.nod_id, d.nod_id)::int8 as nod_id, 
coalesce (abc.dir_id, d.dir_id)::int8 as dir_id, 
coalesce (abc.kato_id, d.kato_id)::int8 as kato_id, 
coalesce (abc.vids_id, d.vids_id)::int8 as vids_id,
coalesce (abc.depo_id, d.depo_id)::int8 as depo_id,
coalesce (abc.dep_id, d.dep_id)::int8 as dep_id
from(
select  
coalesce (ab.org_id, c.org_id) as org_id,
coalesce (ab.dor_kod, c.dor_kod) as dor_kod,
coalesce (ab.date_type_id, c.date_type_id) as date_type_id, 
coalesce (ab.metric_type_id, c.metric_type_id) as metric_type_id, 
coalesce (ab.cargo_type_id, c.cargo_type_id) as cargo_type_id, 
coalesce (ab.val_type_id, c.val_type_id) as val_type_id, 
coalesce (ab.dt, c.dt) as dt, 
(ab.value+c.value)::float8 as value,
coalesce (ab.duch_id, c.duch_id) as duch_id, 
coalesce (ab.nod_id, c.nod_id) as nod_id, 
coalesce (ab.dir_id, c.dir_id) as dir_id, 
coalesce (ab.kato_id, c.kato_id) as kato_id, 
coalesce (ab.vids_id, c.vids_id) as vids_id,
coalesce (ab.depo_id, c.depo_id) as depo_id,
coalesce (ab.dep_id, c.dep_id) as dep_id
from(
select
coalesce (a.org_id, b.org_id) as org_id, 
coalesce (a.dor_kod, b.dor_kod) as dor_kod,  
coalesce (a.date_type_id, b.date_type_id) as date_type_id, 
coalesce (a.metric_type_id, b.metric_type_id) as metric_type_id, 
coalesce (a.cargo_type_id, b.cargo_type_id) as cargo_type_id, 
coalesce (a.val_type_id, b.val_type_id) as val_type_id, 
coalesce (a.dt, b.dt) as dt, 
(a.value-b.value)::float8 as value,
coalesce (a.duch_id, b.duch_id) as duch_id, 
coalesce (a.nod_id, b.nod_id) as nod_id, 
coalesce (a.dir_id, b.dir_id) as dir_id, 
coalesce (a.kato_id, b.kato_id) as kato_id, 
coalesce (a.vids_id, b.vids_id) as vids_id,
coalesce (a.depo_id, b.depo_id) as depo_id,
coalesce (a.dep_id, b.dep_id) as dep_id
from public.la_qa1 a
	full join public.la_qa2 b
		on  a.org_id = b.org_id
		and a.date_type_id = b.date_type_id
		and a.cargo_type_id = b.cargo_type_id
		and a.val_type_id = b.val_type_id
		and a.metric_type_id = b.metric_type_id
		and a.dt = b.dt
		and a.nod_id = b.nod_id
		and a.duch_id = b.duch_id
		and a.vids_id = b.vids_id 
		and a.kato_id = b.kato_id 
		and a.dir_id = b.dir_id
and a.depo_id = b.depo_id
and a.dep_id = b.dep_id) ab
	full join public.la_qa3 c
		on  ab.org_id = c.org_id
		and ab.date_type_id = c.date_type_id
		and ab.cargo_type_id = c.cargo_type_id
		and ab.val_type_id = c.val_type_id
		and ab.metric_type_id = c.metric_type_id
		and ab.dt = c.dt
		and ab.nod_id = c.nod_id
		and ab.duch_id = c.duch_id
		and ab.vids_id = c.vids_id 
		and ab.kato_id = c.kato_id 
		and ab.dir_id = c.dir_id
		and ab.depo_id = c.depo_id
		and ab.dep_id = c.dep_id)abc
	full join public.la_qa4 d
		on 	abc.org_id = d.org_id
		and abc.date_type_id = d.date_type_id
		and abc.cargo_type_id = d.cargo_type_id
		and abc.val_type_id = d.val_type_id
		and abc.metric_type_id = d.metric_type_id
		and abc.dt = d.dt
		and abc.nod_id = d.nod_id
		and abc.duch_id = d.duch_id
		and abc.vids_id = d.vids_id 
		and abc.kato_id = d.kato_id 
		and abc.dir_id = d.dir_id
		and abc.depo_id = d.depo_id
		and abc.dep_id = d.dep_id)abcd
	left join public.la_qa5 e
		on 	abcd.org_id = e.org_id
		and abcd.date_type_id = e.date_type_id
		and abcd.cargo_type_id = e.cargo_type_id
		and abcd.val_type_id = e.val_type_id
		and abcd.metric_type_id = e.metric_type_id
		and abcd.dt = e.dt
		and abcd.nod_id = e.nod_id
		and abcd.duch_id = e.duch_id
		and abcd.vids_id = e.vids_id 
		and abcd.kato_id = e.kato_id 
		and abcd.dir_id = e.dir_id
		and abcd.depo_id = e.depo_id
		and abcd.dep_id = e.dep_id
cross join (select * from dm.d_hcode_t where id = '00053') hcd
    where abcd.%s
    ;
end;
$f$
;""")

query_3_0132 = ("""select * from public.lilo_auto_qa()
except
select  hcode_id, hcode_name, hcode_unit_name, org_id, dor_kod, date_type_id, metric_type_id, cargo_type_id, val_type_id, unit_id, dt, 
		value::numeric(20,6), duch_id, nod_id, dir_id, kato_id, vids_id, depo_id, dep_id from dm_rep.dm_all_indicators_v
where hcode_id = '00053'
and calc_rule = 'ratio'
and %s
""")


QUERYS_3_1 = [v for v in locals() if v.startswith('query')]

QUERYS_3_1_CREATE = [n for n in QUERYS_3_1 if QUERYS_3_1.index(n) % 2 == 0]
QUERYS_3_1_RUN = [n for n in QUERYS_3_1 if QUERYS_3_1.index(n) % 2 != 0]

QUERYS_3_1_CREATE_FUN_EQUAL = [n for n in QUERYS_3_1_CREATE if QUERYS_3_1_CREATE.index(n) % 2 == 0]
QUERYS_3_1_CREATE_FUN_EMPTY = [n for n in QUERYS_3_1_CREATE if QUERYS_3_1_CREATE.index(n) % 2 != 0]

QUERYS_3_1_RUN_EQUAL = [n for n in QUERYS_3_1_RUN if QUERYS_3_1_RUN.index(n) % 2 == 0]
QUERYS_3_1_RUN_EMPTY = [n for n in QUERYS_3_1_RUN if QUERYS_3_1_RUN.index(n) % 2 != 0]

QUERYS_3_1_EQUAL_TUP = zip(QUERYS_3_1_CREATE_FUN_EQUAL,QUERYS_3_1_RUN_EQUAL)
QUERYS_3_1_EMPTY_TUP = zip(QUERYS_3_1_CREATE_FUN_EMPTY,QUERYS_3_1_RUN_EMPTY)

