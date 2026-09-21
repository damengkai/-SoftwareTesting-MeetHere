import json
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.cookiejar import CookieJar
from typing import Any, Dict, Optional


@dataclass
class ApiResponse:
    status_code: int
    text: str
    headers: Dict[str, str]
    url: str

    def json(self) -> Any:
        return json.loads(self.text)


class ApiClient:
    def __init__(self, base_url: str, timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.cookies = CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies)
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> ApiResponse:
        url = self._url(path)
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(url, method="GET")
        return self._send(request)

    def post_form(self, path: str, data: Dict[str, Any]) -> ApiResponse:
        body = urllib.parse.urlencode(data).encode("utf-8")
        request = urllib.request.Request(
            self._url(path),
            data=body,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        return self._send(request)

    def login(self, user_id: str, password: str) -> ApiResponse:
        return self.post_form(
            "/loginCheck.do",
            {"userID": user_id, "password": password},
        )

    def has_cookie(self, name: str) -> bool:
        return any(cookie.name == name for cookie in self.cookies)

    def _url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self.base_url}/{path.lstrip('/')}"

    def _send(self, request: urllib.request.Request) -> ApiResponse:
        try:
            with self.opener.open(request, timeout=self.timeout) as response:
                raw = response.read()
                return ApiResponse(
                    status_code=response.getcode(),
                    text=raw.decode("utf-8", errors="replace"),
                    headers=dict(response.headers.items()),
                    url=response.geturl(),
                )
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            return ApiResponse(
                status_code=exc.code,
                text=raw.decode("utf-8", errors="replace"),
                headers=dict(exc.headers.items()),
                url=exc.geturl(),
            )
