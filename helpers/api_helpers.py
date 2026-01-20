from requests import Session


class ApiSession:
    def __init__(self, session: Session, host):
        self.session = session
        self.host = host

    def _send(self, method: str, endpoint: str, **kwargs):
        response = self.session.request(method, self.host + endpoint, **kwargs)
        return response

    def get(self, endpoint: str, params: dict | None = None, headers: dict | None = None):
        return self._send("GET", endpoint=endpoint, params=params, headers=headers)

    def post(self, endpoint: str, params: dict | None = None, body: dict | None = None, headers: dict | None = None):
        return self._send("POST", endpoint=endpoint, params=params, json=body, headers=headers)

    def put(self, endpoint: str, params: dict | None = None, body: dict | None = None, headers: dict | None = None):
        return self._send("PUT", endpoint=endpoint, params=params, json=body, headers=headers)

    def delete(self, endpoint: str, params: dict | None = None, body: dict | None = None, headers: dict | None = None):
        return self._send("DELETE", endpoint=endpoint, params=params, json=body, headers=headers)
