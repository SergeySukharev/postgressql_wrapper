import allure
import pytest


from SQL_SCRIPTS.INCOME.INC_M_3_1 import *
from SQL_SCRIPTS.INCOME.INC_M_3_2 import *


@allure.feature('INCOME')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', QUERYS_3_2_EQUAL)
def test_equal(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_3'], dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)
    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    line_1 = [n for n in lines if lines.index(n) % 2 == 0]
    line_2 = [n for n in lines if lines.index(n) % 2 != 0]

    for this, next_one in zip(line_1, line_2):
        assert this == next_one


@allure.feature('INCOME')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query', QUERYS_3_2_EMPTY)
def test_empty(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_3'], dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)
    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    assert lines == []


@allure.feature('INCOME with function create')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query, query2', QUERYS_3_1_EQUAL_TUP)
def test_equal_with_fun(connection, query, query2, dates):
    script_create_fun = eval(query) % (dates['date_3'])
    allure.attach(script_create_fun)
    connection.execute(script_create_fun)

    script_with_dates = eval(query2) % (dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)
    lines = connection.fetchall()
    connection.execute('drop function public.lilo_auto_qa();')
    string_lines = str(lines)
    allure.attach(string_lines)

    line_1 = [n for n in lines if lines.index(n) % 2 == 0]
    line_2 = [n for n in lines if lines.index(n) % 2 != 0]

    for this, next_one in zip(line_1, line_2):
        assert this == next_one


@allure.feature('INCOME with function create')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query, query2', QUERYS_3_1_EMPTY_TUP)
def test_empty_with_fun(connection, query, query2, dates):
    script_create_fun = eval(query) % (dates['date_3'])
    allure.attach(script_create_fun)
    connection.execute(script_create_fun)

    script_with_dates = eval(query2) % (dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    connection.execute('drop function public.lilo_auto_qa();')
    assert lines == []
