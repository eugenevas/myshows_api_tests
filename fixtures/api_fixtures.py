import pytest
import requests
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
from helpers.file_helpers import API_SERIES_STATUS_TO_DB_MAPPING
from helpers.api_helpers import ApiSession
from config.api_config import API_HOST


# 1. Фикстура конфигурации
@pytest.fixture(scope='session')
def settings():
    return {
        'db': {
            'dbname': 'my-shows-rating',
            'user': 'postgres',
            'password': '123456',
            'host': API_HOST,
            'port': '5432',
            'connect_timeout': 5,
            'row_factory': psycopg.rows.dict_row,
        },
        'backend_host': API_HOST
    }


# 2. Фикстура api_session
@pytest.fixture(scope='session')
def api_session(settings):
    with requests.Session() as session:
        yield ApiSession(session, settings['backend_host'])


# 3. Фикстура для добавления сериалов в базу (через SQL)
@pytest.fixture
def add_series_in_db(settings):
    connection_params = settings['db']

    # series_list = [
    #     {"name": "Тоннель",
    #      "photo": "https://media.myshows.me/shows/760/e/5a/e5a5fd3587da0300f44d530c323021d5.jpg", "rating": 9,
    #      "status": "Смотрю", "review": "Супер"},
    #     {"name": "Берлинская жара",
    #      "photo": "https://media.myshows.me/shows/760/b/0c/b0ce3a94a79ec38d994a2d551b5e515f.jpg", "rating": 9,
    #      "status": "Посмотрел", "review": "Нечто"},
    #     {"name": "Странные дела",
    #      "photo": "https://media.myshows.me/shows/760/9/15/915b56d169568a7431e671770d426f60.jpg", "rating": 8,
    #      "status": "Буду смотреть", "review": "Держит в напряжении"}
    # ]

    with psycopg.connect(**connection_params) as conn:
        with conn.cursor() as cur:
            # Очистка таблицы
            cur.execute("TRUNCATE TABLE series RESTART IDENTITY CASCADE;")
            conn.commit()
            # Чтение SQL из файла
            # sql = sql_path.read_text(encoding='utf-8')
            # cur.execute(sql)
            conn.execute((Path(__file__).parent.parent / "data" / "insert_series.sql").read_text(encoding='utf-8'))
            conn.commit()
    yield
    # Очистка после теста
    with psycopg.connect(**connection_params) as conn:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE series RESTART IDENTITY CASCADE;")
            conn.commit()


# 4. Фикстура для добавления сериалов через API (посылает POST-запросы)
@pytest.fixture
def add_series_via_api(api_session, settings):
    test_series = [
        {"name": "Тоннель",
         "photo": "https://media.myshows.me/shows/760/e/5a/e5a5fd3587da0300f44d530c323021d5.jpg",
         "rating": 9,
         "status": "Смотрю",
         "review": "Супер"},

        {"name": "Берлинская жара",
         "photo": "https://media.myshows.me/shows/760/b/0c/b0ce3a94a79ec38d994a2d551b5e515f.jpg",
         "rating": 9,
         "status": "Посмотрел",
         "review": "Нечто"},

        {"name": "Очень странные дела",
         "photo": "https://media.myshows.me/shows/760/9/15/915b56d169568a7431e671770d426f60.jpg",
         "rating": 8,
         "status": "Буду смотреть",
         "review": "Держит в напряжении"}
    ]
    for s in test_series:
        response = api_session.post(url="/api/v1/series", json=s)
        response.raise_for_status()
    yield
    # Удаление сериалов через API
    # Тут можно либо хранить ID сериалов, либо запросить список и удалить
    response = api_session.get("/api/v1/series")
    response.raise_for_status()
    series_list = response.json()
    for s in series_list:
        api_session.delete(f"/api/v1/series/{s["id"]}")

# ================================================================


# СТАРЫЙ КОД
# @pytest.fixture
# def add_episodes():
#     # Настройки подключения к базе данных
#     conn_params = {
#         'dbname': 'my-shows-rating',
#         'user': 'postgres',
#         'password': '123456',
#         'host': 'localhost',
#         'port': '5432',
#     }
#
#
#
#     # Тестовые данные - на входе статус в API-значении
#     test_series = [
#         {"id": 6, "name": "Наруто", "photo": "https://media.myshows.me/shows/760/3/e8/3e8e697187b0fdb49941ecf22db5b9b3.jpg", "rating": 9, "status": "Смотрю","review": "Отличный сериал"},
#         {"id": 7, "name": "Мандалорец", "photo": "https://media.myshows.me/shows/760/6/61/66124cb92abfa1ae993d66f2e80463fc.jpg", "rating": 9, "status": "Посмотрел", "review": "Эпично"},
#         {"id": 8, "name": "Союз спасения. Время гнева", "photo": "https://media.myshows.me/shows/760/c/64/c6463ee65ae3aeaf071af0f502befc04.jpg", "rating": 8, "status": "Буду смотреть", "review": "Интересный сюжет"}
#     ]
#
#
#     with psycopg.connect(**conn_params) as conn:
#         with conn.cursor() as cur:
#             # Очищаем полностью таблицу series
#             cur.execute("DELETE FROM series;")
#             # conn.commit()
#             # Вставляем тестовые данные с переводом статуса в базу
#             for s in test_series:
#                 cur.execute("""
#                      INSERT INTO series (id, name, photo, rating, status, review)
#                      VALUES (%s, %s, %s, %s, %s, %s);
#                  """, (s["id"], s["name"], s["photo"], s["rating"], API_SERIES_STATUS_TO_DB_MAPPING[s["status"]],
#                        s["review"]))
#             conn.commit()
#         yield test_series
#         # После теста очищаем таблицу
#         with conn.cursor() as cur:
#             # cur.execute("DELETE FROM series;")
#             conn.commit()


# @pytest.fixture
# def update_episodes():
#     # Настройки подключения к базе данных
#     conn_params = {
#         'dbname': 'my-shows-rating',
#         'user': 'postgres',
#         'password': '123456',
#         'host': 'localhost',
#         'port': '5432',
#     }
#
#     # Тестовые данные - на входе статус в API-значении
#     test_series = {
#         "name": "Naruto",
#         "photo": "https://media.myshows.me/shows/760/3/e8/3e8e697187b0fdb49941ecf22db5b9b3.jpg",
#         "rating": 7,
#         "status": "Посмотрел",
#         "review": "Тестовый отзыв"
#     }
#
#     with psycopg.connect(**conn_params) as conn:
#         with conn.cursor() as cur:
#             cur.execute(
#                 "INSERT INTO series (name, photo, rating, status, review) VALUES (%s, %s, %s, %s, %s) RETURNING id;",
#                 (test_series["name"], test_series["photo"], test_series["rating"],
#                  API_SERIES_STATUS_TO_DB_MAPPING[test_series["status"]], test_series["review"])
#             )
#             series_id = cur.fetchone()[0]
#             # conn.commit()
#
#     yield series_id
#
#     # Удаляем сериал после теста
#     with psycopg.connect(**conn_params) as conn:
#         with conn.cursor() as cur:
#             cur.execute("DELETE FROM series WHERE id = %s;", (series_id,))
#             conn.commit()
