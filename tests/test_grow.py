import allure
import pytest


from SQL_SCRIPTS.GROW.INC_M_2_1_1 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_2 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_3 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_4 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_5 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_6 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_7 import *
from SQL_SCRIPTS.GROW.INC_M_2_1_8 import *

EQUAL_SETS = QUERYS_2_1_1_EQUAL + QUERYS_2_1_2_EQUAL + QUERYS_2_1_3_EQUAL + \
             QUERYS_2_1_4_EQUAL + QUERYS_2_1_5_EQUAL + QUERYS_2_1_6_EQUAL + \
             QUERYS_2_1_7_EQUAL + QUERYS_2_1_8_EQUAL


EMPTY_SETS = QUERYS_2_1_1_EMPTY + QUERYS_2_1_2_EMPTY + QUERYS_2_1_3_EMPTY + \
             QUERYS_2_1_4_EMPTY + QUERYS_2_1_5_EMPTY + QUERYS_2_1_6_EMPTY + \
             QUERYS_2_1_7_EMPTY + QUERYS_2_1_8_EMPTY


@allure.feature('GROW')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', EQUAL_SETS)
def test_equal(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_1'], dates['date_1'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    line_1 = [n for n in lines if lines.index(n) % 2 == 0]
    line_2 = [n for n in lines if lines.index(n) % 2 != 0]

    for this, next_one in zip(line_1, line_2):
        assert this[1] == next_one[1]


@allure.feature('GROW')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query', EMPTY_SETS)
def test_empty(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_1'], dates['date_1'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    assert lines == []
