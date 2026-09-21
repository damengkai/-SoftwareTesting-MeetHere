import os
import re
from pathlib import Path
from typing import Any

import yaml


ENV_PATTERN = re.compile(r"\$\{([A-Z0-9_]+)(?::([^}]*))?\}")
REQUIRED_CASE_FIELDS = {"id", "name", "module", "priority", "request", "assertions"}


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    case_path = Path(path)
    with case_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, list):
        raise ValueError(f"Case file must contain a YAML list: {case_path}")

    cases = _resolve_env(data)
    for index, case in enumerate(cases, start=1):
        _validate_case(case, index, case_path)
    return cases


def _validate_case(case: Any, index: int, case_path: Path) -> None:
    if not isinstance(case, dict):
        raise ValueError(f"Case #{index} must be a mapping in {case_path}")

    missing = REQUIRED_CASE_FIELDS - case.keys()
    if missing:
        fields = ", ".join(sorted(missing))
        raise ValueError(f"Case #{index} is missing fields [{fields}] in {case_path}")

    request = case["request"]
    if not isinstance(request, dict) or not {"method", "path"} <= request.keys():
        raise ValueError(
            f"Case {case['id']} request must contain method and path"
        )


def _resolve_env(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _resolve_env(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_resolve_env(item) for item in value]
    if isinstance(value, str):
        return ENV_PATTERN.sub(_replace_env, value)
    return value


def _replace_env(match: re.Match[str]) -> str:
    name = match.group(1)
    default = match.group(2) or ""
    return os.getenv(name, default)
