import psycopg2
import pytest
from dategenerator import DateGenerator


def pytest_addoption(parser):
    parser.addoption(
        "--contur",
        action="store",
        default="rnd_uat",
        help="Chose testing contur example skim, by default rnd_uat"
    )
    parser.addoption(
        "--date_type",
        action="store",
        default="inc_v2",
        help="Chose time type three options:inc_v2,inc_v3,full by default - inc_v2"
    )


@pytest.fixture
def connection(request):
    if request.config.getoption('--contur') == 'rnd_uat':
        con = psycopg2.connect(
            database="rnd_uat",
            user="skim_qa2_etl_srv",
            password="skim_qa2_etl_srv123",
            host="10.248.96.23",
            port="5432",
            options="-c statement_timeout=600s"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        def fin():
            cur.close()
            con.close()

        request.addfinalizer(fin)
        return cur
    elif request.config.getoption('--contur') == 'dev':
        con = psycopg2.connect(
            database="dev",
            user="skim_qa2_etl_srv",
            password="skim_qa_etl_srv123",
            host="10.248.96.23",
            port="5432",
            options="-c statement_timeout=600s"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        def fin():
            cur.close()
            con.close()

        request.addfinalizer(fin)
        return cur
    elif request.config.getoption('--contur') == 'skim':
        con = psycopg2.connect(
            database="skim",
            user="skim_qa2_etl_srv",
            password="skim_qa2_etl_srv123",
            host="10.248.96.23",
            port="5432",
            options="-c statement_timeout=600s"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        def fin():
            cur.close()
            con.close()

        request.addfinalizer(fin)
        return cur
    elif request.config.getoption('--contur') == 'pretest':
        con = psycopg2.connect(
            database="pretest",
            user="skim_qa2_etl_srv",
            password="skim_qa2_etl_srv123",
            host="10.248.96.23",
            port="5432",
            options="-c statement_timeout=600s"
        )
        cur = con.cursor()
        cur.execute('set enable_nestloop to off;')
        cur.execute('set enable_mergejoin to off;')

        def fin():
            cur.close()
            con.close()

        request.addfinalizer(fin)
        return cur


@pytest.fixture(scope="session")
def dates(request):
    if request.config.getoption('--date_type') == 'inc_v2':
        dates = {
            'date_1': f'dt in {DateGenerator.DATE_1}',
            'date_2': f'dt in {DateGenerator.DATE_2}',
            'date_3': f'dt in {DateGenerator.DATE_3}'
        }
        return dates
    elif request.config.getoption('--date_type').startswith('20'):
        time = request.config.getoption('--date_type')
        dates = {
            'date_1': f"dt in{tuple(time.split(','))}",
            'date_2': f"dt in{tuple(time.split(','))}",
            'date_3': f"dt in{tuple(time.split(','))}"
        }
        return dates
    elif request.config.getoption('--date_type') == 'full':
        dates = {
            'date_1': "dt is not null",
            'date_2': "dt is not null",
            'date_3': "dt is not null"
        }
        return dates
