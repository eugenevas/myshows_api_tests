import requests
import pytest
import psycopg

from http import HTTPStatus
from config.api_config import BASE_URL
from helpers.file_helpers import API_SERIES_STATUS_TO_DB_MAPPING
from helpers.file_helpers import FIELDS_TO_TEST
from helpers.file_helpers import EXPECTED_SERIES


class TestGetEndpoint:
    def test_get_episode(self, add_series_in_db, api_session):
        # Вызов фикстуры
        # expected_episodes = add_episodes
        # expected_episodes = add_series_in_db

        url_get_episode = BASE_URL + "/api/v1/series"

        response = api_session.get(url_get_episode)
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        # Преобразуем статус из БД в статус из API через обратный маппинг
        DB_TO_API_STATUS_MAPPING = {v: k for k, v in API_SERIES_STATUS_TO_DB_MAPPING.items()}

        # Создаем вспомогательный словарь для поиска сериалов по имени
        series_by_name = {s["name"]: s for s in body}

        expected_series = EXPECTED_SERIES

        for expected in expected_series:
            assert expected["name"] in series_by_name
            actual = series_by_name[expected["name"]]
            assert actual["name"] == expected["name"]
            assert actual["photo"] == next(s["photo"] for s in expected_series if s["name"] == expected["name"])
            expected_rating = next(s["rating"] for s in expected_series if s["name"] == expected["name"])
            # assert abs(actual["rating"] - expected_rating) < 0.01


# class TestPutEndpoint:
#     # Проверка изменения всех полей по отдельности
#     @pytest.mark.parametrize("field, new_value", FIELDS_TO_TEST)
#     def test_update_series_field(self, update_episodes, field, new_value):
#         series_id = update_episodes  # получение id сериалов из фикстуры
#
#         # Собираем частичный body для обновления
#         update_data = {}
#         update_data[field] = new_value
#
#         url = f"{BASE_URL}/api/v1/series/{series_id}"
#
#         # Выполняем PUT-запрос
#         response = requests.put(url, json=update_data)
#         assert response.status_code == HTTPStatus.OK, f"Failed to update field {field}"
#
#         # После обновления проверяем, что в базе поле изменилось
#         # подключение к базе для проверки
#         conn_params = {
#             'dbname': 'my-shows-rating',
#             'user': 'postgres',
#             'password': '123456',
#             'host': 'localhost',
#             'port': '5432',
#         }
#
#         with psycopg.connect(**conn_params) as conn:
#             with conn.cursor() as cur:
#                 cur.execute("SELECT name, photo, rating, status, review FROM series WHERE id = %s", (series_id,))
#                 row = cur.fetchone()
#                 # Мап полей
#                 db_values = {
#                     "name": row[0],
#                     "photo": row[1],
#                     "rating": row[2],
#                     "status": row[3],
#                     "review": row[4]
#                 }
#                 # Проверяем, что изменилось именно нужное поле
#                 # Внутри теста пригодится использовать правильные названия
#                 # Для этого сделаем общий геттер
#                 expected_value = new_value
#                 actual_value = db_values[field]
#
#                 # Для поля status — оно, возможно, хранится как статус DB, а в API — как строка.
#                 if field == "status":
#                     # сравниваем напрямую со строкой
#                     assert actual_value == API_SERIES_STATUS_TO_DB_MAPPING[new_value], \
#                         f"Expected status {API_SERIES_STATUS_TO_DB_MAPPING[new_value]}, got {actual_value}"
#                 elif field == "rating":
#                     # float comparison
#                     assert abs(actual_value - new_value) < 0.01
#                 else:
#                     assert actual_value == expected_value
