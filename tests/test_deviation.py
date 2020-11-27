import allure
import pytest


from SQL_SCRIPTS.DEVIATION.INC_M_4_1 import *
from SQL_SCRIPTS.DEVIATION.INC_M_4_2 import *
from SQL_SCRIPTS.DEVIATION.INC_M_4_3 import *

EQUAL_SETS = QUERYS_4_1_EQUAL + QUERYS_4_2_EQUAL + QUERYS_4_3_EQUAL
EMPTY_SETS = QUERYS_4_1_EMPTY + QUERYS_4_2_EMPTY + QUERYS_4_3_EMPTY


@allure.feature('Deviation')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', EQUAL_SETS)
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
        if len(this) == 3:
            assert this[2] == next_one[2]
        elif len(this) == 2:
            assert this[1] == next_one[1]
        elif len(this) == 1:
            assert this[0] == next_one[0]
        else:
            assert this == next_one


@allure.feature('Deviation')
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
