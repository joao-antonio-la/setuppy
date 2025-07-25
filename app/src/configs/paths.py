import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Paths:
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    ASSETS_DIR: str = os.path.join(BASE_DIR, "app", "assets")
    DATA_DIR: str = os.path.join(BASE_DIR, "data")

    SETTINGS_JSON_FILE: str = os.path.join(DATA_DIR, "settings.json")
    SETUPS_JSON_FILE: str = os.path.join(DATA_DIR, "setups.json")
    INITIALIZED_FLAG_FILE: str = os.path.join(DATA_DIR, ".initialized")
