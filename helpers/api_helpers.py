import json
import re
import time
from http import HTTPStatus

import requests
from requests import Session


class ApiSession:
    def __init__(self, session: Session, host):
        self.session = session
        self.host = host

    def _send(self, method: str, url: str, **kwargs):
        timestamp = time.time() + 5
        while time.time() < timestamp:
            response = self.session.request(method=method, url=url, **kwargs)
            response_body = response.json()
            if response.status_code == HTTPStatus.BAD_REQUEST and response_body["message"] == "Лимит запросов превышен":
                time.sleep(1)
            else:
                break
        else:
            raise AssertionError("Не удалось прорваться через Rate Limiter")
        return response

    def get(self, url: str, params: dict | None = None, headers: dict | None = None):
        return self._send("GET", url=url, params=params, headers=headers)

    def post(self, url: str, params: dict | None = None, json: dict | None = None, headers: dict | None = None):
        return self._send("POST", url=url, params=params, json=json, headers=headers)

    def delete(self, url: str, params: dict | None = None, json: dict | None = None, headers: dict | None = None):
        return self._send("DELETE", url=url, params=params, json=json, headers=headers)
