from pathlib import Path
from tarfile import data_filter

import pytest
import requests

from config.api_config import BASE_URL, SERIES_ENDPOINT
from data.series_for_testing import SERIES_FOR_TEST
from helpers.api_helpers import ApiSession
from helpers.db_helpers import DbConnection
from config.bd_config import Config


# 1. Фикстура конфигурации
@pytest.fixture(scope='session')
def settings_db():
    db_conn = DbConnection(Config())
    with db_conn:
        yield db_conn


# 2. Фикстура api_session
@pytest.fixture(scope='session')
def api_session():
    with requests.Session() as session:
        yield ApiSession(session, BASE_URL)


# 3. Фикстура для добавления трёх сериалов в базу (через SQL)
@pytest.fixture
def add_series_in_db(settings_db):
    with settings_db:
        # settings_db.execute(f"TRUNCATE TABLE public.series")

        settings_db.execute((Path(__file__).parent.parent / "data" / "insert_series_3.sql").read_text(encoding='utf-8'))
        # series = result.fetchone()
        # yield dict(series)
        yield

        # После теста — удалить сериалы
        settings_db.execute((Path(__file__).parent.parent / "data" / "delete_series_3.sql").read_text(encoding='utf-8'))


# В эту фикстуру добавляются сначала 1 сериал, потом 3 сериала
@pytest.fixture
def add_exact_number_of_series_in_db(settings_db, request):
    count = getattr(request, "param", 0)
    # Очищаем таблицу перед тестом
    with settings_db:
        # settings_db.execute(f"TRUNCATE TABLE public.series")

        # Если количество строк больше 1, то добавляем сериал в таблицу
        if count > 0:
            sql_file_name = f"insert_series_{count}.sql"
            settings_db.execute((Path(__file__).parent.parent / "data" / sql_file_name).read_text(encoding="utf-8"))

        yield count
        # teardown: очищаем таблицу после теста
        settings_db.execute(f"TRUNCATE TABLE public.series")



# фикстура на добавление одной серии
@pytest.fixture
def add_1_series_returning_id_in_db(settings_db):
    with settings_db:
        series_dict = settings_db.execute(
            (Path(__file__).parent.parent / "data" / "insert_series_1.sql").read_text(encoding='utf-8')
        ).fetchone()
        yield series_dict
        settings_db.execute(f"DELETE FROM public.series WHERE id IN ({series_dict["id"]})")



    # with settings_db:
    #     settings_db.execute((Path(__file__).parent.parent / "data" / "insert_series_1.sql").read_text(encoding='utf-8'))
    #     yield
    #     settings_db.execute((Path(__file__).parent.parent / "data" / "delete_series_1.sql").read_text(encoding='utf-8'))
# фикстура на добавление одной серии

# 4.Фикстура для добавления сериалов через API (посылает POST-запросы)
@pytest.fixture
def add_series_via_api(api_session):
    created_series_ids_list = []
    for s in SERIES_FOR_TEST:
        response = api_session.post(endpoint=SERIES_ENDPOINT, body=s)
        response.raise_for_status()
        created_series_ids_list.append(response.json()["id"])
    yield
    # Удаление сериалов через API
    for id_ in created_series_ids_list:
        api_session.delete(f"{SERIES_ENDPOINT}/{id_}")


@pytest.fixture
def fixture_type(request):
    request.getfixturevalue(request.param)