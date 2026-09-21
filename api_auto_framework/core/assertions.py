from typing import Any, Iterable


class ApiAssertions:
    @staticmethod
    def status_in(actual: int, expected: Iterable[int]) -> None:
        expected_values = list(expected)
        assert actual in expected_values, (
            f"Expected status code in {expected_values}, got {actual}"
        )

    @staticmethod
    def text_equals(actual: str, expected: str) -> None:
        assert actual == expected, f"Expected text {expected!r}, got {actual!r}"

    @staticmethod
    def text_contains(actual: str, expected: str) -> None:
        assert expected in actual, f"Expected response text to contain {expected!r}"

    @staticmethod
    def cookie_exists(client: Any, cookie_name: str) -> None:
        assert client.has_cookie(cookie_name), f"Expected cookie {cookie_name!r}"

    @staticmethod
    def json_type(response: Any, expected_type: str) -> None:
        body = response.json()
        type_map = {
            "list": list,
            "dict": dict,
        }
        if expected_type not in type_map:
            raise AssertionError(f"Unsupported expected JSON type: {expected_type}")
        assert isinstance(body, type_map[expected_type]), (
            f"Expected JSON type {expected_type}, got {type(body).__name__}"
        )
