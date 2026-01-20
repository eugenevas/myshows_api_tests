from http import HTTPStatus

import pytest


from config.api_config import SERIES_ENDPOINT
from data.series_for_testing import SERIES_FOR_TEST
from helpers.db_mapping import API_SERIES_STATUS_TO_DB_MAPPING


from helpers.file_helpers import load_yaml
from jsonschema import validate


DB_TO_API_STATUS_MAPPING = {v: k for k, v in API_SERIES_STATUS_TO_DB_MAPPING.items()}


class TestGetEndpoint:
    @pytest.mark.parametrize("fixture_type", ["add_series_via_api", "add_series_in_db"], indirect=True)
    def test_write_series_in_bd_get_episode(self, fixture_type, api_session, check):
        response = api_session.get(SERIES_ENDPOINT)
        assert response.status_code == HTTPStatus.OK
        body = response.json()

        # Создаем вспомогательный словарь для поиска сериалов по имени
        series_by_name = {s["name"]: s for s in body}

        for s in SERIES_FOR_TEST:
            check.is_in(s["name"], series_by_name, f'Series {s["name"]} should be in response')
            actual = series_by_name.get(s["name"])
            if actual:
                check.equal(actual["photo"], s["photo"], f"Photo for {s['name']}")
                check.equal(actual["rating"], s["rating"], f"Rating for {s['name']}")
                check.equal(actual["review"], s["review"], f"Review for {s['name']}")
                check.equal(actual["status"], s["status"], f"Status for {s['name']}")


    @pytest.mark.parametrize( "series_in_db", [0, 1, 3], indirect=True)
    def test_compare_series_lines(self, series_in_db, api_session):
        expected_count = series_in_db

        response = api_session.get(SERIES_ENDPOINT)
        response.raise_for_status()

        body = response.json()

        assert response.status_code == HTTPStatus.OK
        assert len(body) == expected_count

        template = load_yaml("myshows_get.yml")
        validate(body, template)

class TestPutEndpoint:
    @pytest.mark.parametrize(
        "field, new_value",
        [
            ("name", "Наруто"),
            ("photo", "https://media.myshows.me/shows/760/9/93/9930aab53a0e8b5176a5d13d530511c3.jpg"),
            ("rating", 10),
            ("status", "Буду смотреть"),
            ("review", "Отзыыыыв")
        ]
    )
    def test_update_series(self, api_session, settings_db, add_series_in_db, field, new_value):
        cursor = settings_db.connection.cursor()

        # Получаем сериал из БД
        cursor.execute("""
                    SELECT id, name, status, photo, rating, review
                    FROM public.series
                    WHERE name = 'Наруто'
                """)
        series = dict(cursor.fetchone())
        series_id = series["id"]

        # Конвертируем статус из БД в API-формат
        if "status" in series:
            series["status"] = DB_TO_API_STATUS_MAPPING.get(series["status"], series["status"])

        # Меняем только нужное поле
        series[field] = new_value


        response = api_session.put(
            endpoint=f"{SERIES_ENDPOINT}/{series_id}",
            body=series
        )

        # --- assert API ---
        assert response.status_code == HTTPStatus.OK, f"Response body: {response.text}"

        # --- assert DB ---
        cursor.execute(f"SELECT {field} FROM public.series WHERE id = %s", (series_id,))
        db_value = cursor.fetchone()[field]

        # Если поле status — конвертируем в API-формат для сравнения
        if field == "status":
            db_value = DB_TO_API_STATUS_MAPPING.get(db_value, db_value)

        assert db_value == new_value