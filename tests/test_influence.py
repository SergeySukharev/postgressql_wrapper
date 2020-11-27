import allure
import pytest


from SQL_SCRIPTS.INFLUENCE.INC_M_5_1 import *
from SQL_SCRIPTS.INFLUENCE.INC_M_5_2 import *
from SQL_SCRIPTS.INFLUENCE.INC_M_5_3 import *

EQUAL_SETS = QUERYS_5_1_EMPTY + QUERYS_5_2_EMPTY + QUERYS_5_3_EMPTY
EMPTY_SETS = QUERYS_5_1_EQUAL + QUERYS_5_2_EQUAL + QUERYS_5_3_EQUAL


@allure.feature('Influence')
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


@allure.feature('Influence')
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
