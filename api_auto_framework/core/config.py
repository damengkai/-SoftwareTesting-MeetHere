import configparser
import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT_DIR / "config" / "config.ini"


@dataclass(frozen=True)
class Settings:
    base_url: str
    timeout: int
    user_id: str
    user_password: str
    admin_id: str
    admin_password: str


def load_settings() -> Settings:
    parser = configparser.ConfigParser()
    parser.read(CONFIG_PATH, encoding="utf-8")

    return Settings(
        base_url=os.getenv("MEETHERE_BASE_URL", parser.get("api", "base_url")),
        timeout=int(os.getenv("MEETHERE_TIMEOUT", parser.get("api", "timeout"))),
        user_id=os.getenv("MEETHERE_USER_ID", parser.get("user", "user_id")),
        user_password=os.getenv(
            "MEETHERE_USER_PASSWORD", parser.get("user", "password")
        ),
        admin_id=os.getenv("MEETHERE_ADMIN_ID", parser.get("admin", "user_id")),
        admin_password=os.getenv(
            "MEETHERE_ADMIN_PASSWORD", parser.get("admin", "password")
        ),
    )
