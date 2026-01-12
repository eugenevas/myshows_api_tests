from http import HTTPStatus

import pytest

from config.api_config import SERIES_ENDPOINT
from data.series_for_testing import SERIES_FOR_TEST


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