import allure
import pytest

from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_1and2 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_3 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_3_FUN import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_4 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_5 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_6 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_7 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_8 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_9 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_10 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_11 import *
from SQL_SCRIPTS.GROW_PLAN.INC_M_2_2_13 import *

EQUAL_SETS = QUERYS_2_1_2_EQUAL + QUERYS_2_3_EQUAL + QUERYS_2_4_EQUAL + \
             QUERYS_2_5_EQUAL + QUERYS_2_6_EQUAL + QUERYS_2_7_EQUAL + \
             QUERYS_2_8_EQUAL + QUERYS_2_9_EQUAL + QUERYS_2_10_EQUAL + \
             QUERYS_2_11_EQUAL

EMPTY_SETS = QUERYS_2_1_2_EMPTY + QUERYS_2_3_EMPTY + QUERYS_2_4_EMPTY + QUERYS_2_5_EMPTY + \
             QUERYS_2_6_EMPTY + QUERYS_2_7_EMPTY + QUERYS_2_8_EMPTY + \
             QUERYS_2_9_EMPTY + QUERYS_2_10_EMPTY + QUERYS_2_11_EMPTY



@allure.feature('GROW_PLAN')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', EQUAL_SETS)
def test_equal(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_2'], dates['date_2'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    line_1 = []
    line_2 = []
    for item in lines:
        if item[0] == 'tgt':
            line_1.append(item)
        else:
            line_2.append(item)
    for this, next_one in zip(line_1, line_2):
        assert this[1] == next_one[1]


@allure.feature('GROW_PLAN')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query', EMPTY_SETS)
def test_empty(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_2'], dates['date_2'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    assert lines == []


@allure.feature('GROW_PLAN')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', QUERYS_2_13)
def test_equal_2_13(connection, query, dates):
    # Надо заменить на один имеенованный аргумент
    script_with_dates = eval(query) % (dates['date_2'], dates['date_2'],
                                       dates['date_2'], dates['date_2'], dates['date_2'],
                                       dates['date_2'], dates['date_2'], dates['date_2'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    line_1 = []
    line_2 = []
    for item in lines:
        if item[0] == 'tgt':
            line_1.append(item)
        else:
            line_2.append(item)
    for this, next_one in zip(line_1, line_2):
        assert this[1] == next_one[1]


@allure.feature('GROW_PLAN')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query, query2', QUERYS_2_3_3)
def test_empty_with_fun(connection, query, query2, dates):
    script_create_fun = eval(query) % (dates['date_2'])
    allure.attach(script_create_fun)
    connection.execute(script_create_fun)

    script_with_dates = eval(query2) % (dates['date_2'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    connection.execute('drop function public.lilo_auto_qa();')
    assert lines == []
