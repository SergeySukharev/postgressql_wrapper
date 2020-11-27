import allure
import pytest


from SQL_SCRIPTS.OVERDRAFT.INC_M_7_1 import *
from SQL_SCRIPTS.OVERDRAFT.INC_M_7_2 import *
from SQL_SCRIPTS.OVERDRAFT.INC_M_7_3 import *

EQUAL_SETS = QUERYS_7_1_EMPTY + QUERYS_7_2_EMPTY + QUERYS_7_3_EMPTY
EMPTY_SETS = QUERYS_7_1_EQUAL + QUERYS_7_2_EQUAL + QUERYS_7_3_EQUAL


@allure.feature('Overdraft')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', EQUAL_SETS)
def test_equal(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_3'], dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    line_1 = []
    line_2 = []
    for item in lines:
        if item[0] == 'calc':
            line_1.append(item)
        else:
            line_2.append(item)
    for this, next_one in zip(line_1, line_2):
        assert this[2] == next_one[2]


@allure.feature('Overdraft')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query', EMPTY_SETS)
def test_empty(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_3'], dates['date_3'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)

    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)
    assert lines == []
