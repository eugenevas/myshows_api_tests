from http import HTTPStatus
import requests
import pytest


from config.api_config import BASE_URL
from helpers.file_helpers import API_SERIES_STATUS_TO_DB_MAPPING


class TestGetEndpoint:
    def test_get_episode(self, add_episodes):
        # Вызов фикстуры
        expected_episodes = add_episodes

        url_get_episode = BASE_URL + "/api/v1/series"

        response = requests.get(url=url_get_episode)
        assert response.status_code == HTTPStatus.OK
        # body = response.json()
        print(response.text)
        body = response.json()

        # Преобразуем статус из БД в статус из API через обратный маппинг
        DB_TO_API_STATUS_MAPPING = {v: k for k, v in API_SERIES_STATUS_TO_DB_MAPPING.items()}

        # Проверим, что пришедшие данные совпадают с тем, что в фикстуре, по ключевым полям
        # Учтём, что статус из базы - уже переведены в API-значения
        response_series_by_id = {item["id"]: item for item in body}

        for expected in expected_episodes:
            assert expected["id"] in response_series_by_id
            got = response_series_by_id[expected["id"]]

            assert got["name"] == expected["name"]
            assert got["photo"] == expected["photo"]
            assert abs(got["rating"] - expected["rating"]) < 0.01  # плавающая точность
            # статус в ответе должен соответствовать API-значению
            # assert got["status"] == DB_TO_API_STATUS_MAPPING[expected["status"]]
            assert got["status"] == expected["status"]
            assert got["review"] == expected["review"]