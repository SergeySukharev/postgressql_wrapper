import allure
import pytest
from SQL_SCRIPTS.TOTAL_REJECTS.INC_M_2_3 import *


@allure.feature('Total_rejects')
@allure.story('Сравнение всех записей')
@pytest.mark.parametrize('query', QUERYS_7_1_EQUAL)
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


@allure.feature('Total_rejects')
@allure.story('Полная сверка')
@pytest.mark.parametrize('query', QUERYS_7_1_EMPTY)
def test_empty(connection, query, dates):
    script_with_dates = eval(query) % (dates['date_2'], dates['date_2'])
    allure.attach(script_with_dates)
    connection.execute(script_with_dates)
    lines = connection.fetchall()
    string_lines = str(lines)
    allure.attach(string_lines)

    assert lines == []
