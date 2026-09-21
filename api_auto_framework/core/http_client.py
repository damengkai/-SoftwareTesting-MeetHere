import json
from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class ApiResponse:
    status_code: int
    text: str
    headers: dict[str, str]
    url: str
    elapsed_ms: float
    error: str | None = None

    def json(self) -> Any:
        return json.loads(self.text)


class HttpClient:
    """MeetHere HTTP client that keeps cookies in one requests session."""

    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": "MeetHere-Pytest-Automation/1.0"}
        )

    def get(self, path: str, params: dict[str, Any] | None = None) -> ApiResponse:
        return self.request("GET", path, params=params)

    def post_form(
        self, path: str, data: dict[str, Any] | None = None
    ) -> ApiResponse:
        return self.request("POST", path, data=data)

    def post_json(
        self, path: str, json_data: dict[str, Any] | None = None
    ) -> ApiResponse:
        return self.request("POST", path, json_data=json_data)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> ApiResponse:
        url = self._build_url(path)
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                data=data,
                json=json_data,
                headers=headers,
                timeout=self.timeout,
            )
            if response.encoding is None:
                response.encoding = "utf-8"
            return ApiResponse(
                status_code=response.status_code,
                text=response.text,
                headers=dict(response.headers),
                url=response.url,
                elapsed_ms=response.elapsed.total_seconds() * 1000,
            )
        except requests.RequestException as exc:
            return ApiResponse(
                status_code=0,
                text="",
                headers={},
                url=url,
                elapsed_ms=0,
                error=str(exc),
            )

    def login(self, user_id: str, password: str) -> ApiResponse:
        return self.post_form(
            "/loginCheck.do",
            {"userID": user_id, "password": password},
        )

    def has_cookie(self, name: str) -> bool:
        return name in self.session.cookies

    def close(self) -> None:
        self.session.close()

    def _build_url(self, path: str) -> str:
        if path.startswith(("http://", "https://")):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"
