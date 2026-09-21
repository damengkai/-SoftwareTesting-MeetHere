from typing import Any

import pytest

from api_auto_framework.core.assertions import ApiAssertions
from api_auto_framework.core.case_loader import load_cases
from api_auto_framework.core.config import ROOT_DIR
from api_auto_framework.core.http_client import ApiResponse, HttpClient


CASE_PATH = ROOT_DIR / "cases" / "smoke_cases.yaml"
CASES = load_cases(CASE_PATH)


def _pytest_case(case: dict[str, Any]):
    marker_names = [*case.get("marks", []), case["priority"].lower()]
    markers = [getattr(pytest.mark, name) for name in marker_names]
    return pytest.param(
        case,
        id=f"{case['id']}-{case['name']}",
        marks=markers,
    )


@pytest.mark.parametrize("case", [_pytest_case(case) for case in CASES])
def test_meethere_api(case: dict[str, Any], request: pytest.FixtureRequest) -> None:
    session_name = case.get("session", "anonymous")
    fixture_name = f"{session_name}_client"
    if fixture_name not in {"anonymous_client", "user_client", "admin_client"}:
        pytest.fail(f"Unsupported session: {session_name}")

    client: HttpClient = request.getfixturevalue(fixture_name)
    response = _send_case(client, case["request"])
    if response.error:
        pytest.fail(f"HTTP request failed: {response.error}")

    _assert_case(client, response, case["assertions"])


def _send_case(client: HttpClient, request_data: dict[str, Any]) -> ApiResponse:
    method = request_data["method"].upper()
    path = request_data["path"]
    if method == "GET":
        return client.get(path, request_data.get("params"))
    if method == "POST_FORM":
        return client.post_form(path, request_data.get("form"))
    if method == "POST_JSON":
        return client.post_json(path, request_data.get("json"))
    raise AssertionError(f"Unsupported method: {method}")


def _assert_case(
    client: HttpClient,
    response: ApiResponse,
    assertions: list[dict[str, Any]],
) -> None:
    for assertion in assertions:
        if "status_in" in assertion:
            ApiAssertions.status_in(response.status_code, assertion["status_in"])
        elif "text_equals" in assertion:
            ApiAssertions.text_equals(response.text.strip(), assertion["text_equals"])
        elif "text_contains" in assertion:
            ApiAssertions.text_contains(response.text, assertion["text_contains"])
        elif "cookie_exists" in assertion:
            ApiAssertions.cookie_exists(client, assertion["cookie_exists"])
        elif "json_type" in assertion:
            ApiAssertions.json_type(response, assertion["json_type"])
        else:
            raise AssertionError(f"Unsupported assertion: {assertion}")
