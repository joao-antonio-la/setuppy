import flet as ft
import json
import os

from dataclasses import dataclass
from enum import Enum

from .paths import Paths
from .styles import Themes, UIScales


class Settings:
    def __init__(self, page: ft.Page):
        self.page = page
        self.loading_errors = []
        self.first_time = not os.path.exists(Paths.INITIALIZED_FLAG_FILE)
        self._data = self.load_settings()
        self.set_settings(self._data)
        self.std_settings = self.get_std_settings()

    @staticmethod
    def get_std_settings() -> dict:
        return {
              "ColorTheme": "green",
              "LaunchOnSystemBoot": False,
              "ShowStepsOutput": True,
              "SystemNotifications": False,
              "SoundAlerts": False,
              "UIScale": "small",
              "ErrorHandlingStrategy": "continue",
              "StepsInterval": 1000,
              "DefaultSetupsFile": Paths.SETUPS_JSON_FILE,
        }
    
    def _fallback_to_std_settings(self) -> dict:
        fallback = self.get_std_settings()
        self.set_settings(fallback)
        self.save_settings()
        self.mark_initialized()
        return fallback
    
    def mark_initialized(self):
        try:
            with open(Paths.INITIALIZED_FLAG_FILE, "w") as f:
                f.write("initialized")
        except Exception:
            pass

    def set_settings(self, settings: dict):
        self.color_theme = settings["ColorTheme"]
        self.launch_on_system_boot = settings["LaunchOnSystemBoot"]
        self.show_steps_output = settings["ShowStepsOutput"]
        self.system_notifications = settings["SystemNotifications"]
        self.sound_alerts = settings["SoundAlerts"]
        self.ui_scale = settings["UIScale"]
        self.error_handling_strategy = settings["ErrorHandlingStrategy"]
        self.steps_interval = settings["StepsInterval"]
        self.default_setups_file = settings["DefaultSetupsFile"]

    def to_dict(self) -> dict:
        return {
            "ColorTheme": self.color_theme,
            "LaunchOnSystemBoot": self.launch_on_system_boot,
            "ShowStepsOutput": self.show_steps_output,
            "SystemNotifications": self.system_notifications,
            "SoundAlerts": self.sound_alerts,
            "UIScale": self.ui_scale,
            "ErrorHandlingStrategy": self.error_handling_strategy,
            "StepsInterval": self.steps_interval,
            "DefaultSetupsFile": self.default_setups_file,
        }

    def load_settings(self) -> dict:
        if self.first_time:
            return self._fallback_to_std_settings()

        try:
            with open(Paths.SETTINGS_JSON_FILE, "r") as settings_file:
                user_settings = json.load(settings_file)
                result = self.check_missing_keys(self.get_std_settings(), user_settings)

                if result != MissingKeys.NONE:
                    self.set_settings(user_settings)
                    self.save_settings()
                    self.loading_errors.append(
                        "Some settings were missing.\n" \
                        "Fixing with standard hard-coded settings.\n" \
                        "Please refrain from manually modifying the settings file."
                    )

                return user_settings

        except FileNotFoundError:
            self.loading_errors.append(
                "Settings file not found.\n" \
                "Loading standard hard-coded settings.\n" \
                "Please refrain from manually modifying the settings file."
            )

        except json.JSONDecodeError:
            self.loading_errors.append(
                "An error ocurred while parsing the JSON settings file.\n" \
                "Fixing with standard hard-coded settings.\n" \
                "Please refrain from manually modifying the settings file."
            )
            
        except Exception as e:
            self.loading_errors.append(
                "Unexpected error loading settings:\n" + e
            )

        return self._fallback_to_std_settings()

    def save_settings(self) -> bool:
        settings_dict: dict = self.to_dict()

        folder = os.path.dirname(Paths.SETTINGS_JSON_FILE)
        os.makedirs(folder, exist_ok=True)

        try:
            with open(Paths.SETTINGS_JSON_FILE, "w") as settings_file:
                json.dump(settings_dict, settings_file, indent=4)
            return True
        except Exception as e:
            return False

    def check_missing_keys(self, std_settings: dict, user_settings: dict) -> str:
        if not user_settings:
            user_settings.update(std_settings)
            return MissingKeys.ALL

        missing_keys = [key for key in std_settings if key not in user_settings]
        for key in missing_keys:
            user_settings[key] = std_settings[key]

        return MissingKeys.SOME if missing_keys else MissingKeys.NONE



class ThemeManager:
    def __init__(self, settings: Settings):
        self.elements = []
        self.settings = settings
        self.current_view = None
        self.theme = Themes.get_theme(settings.color_theme)
        self.ui_scale = UIScales.get_ui_scale(settings.ui_scale)

    def register(self, element: ft.Control):
        self.elements.append(element)

    def set_current_view(self, view: ft.View):
        self.current_view = view
        self.current_view.bgcolor = self.theme.BG
        self.current_view.padding = self.ui_scale.PAGE_PADDING

    def update(self):
        for element in self.elements:
            if hasattr(element, "apply_theme"):
                element.apply_theme(self)

        if self.current_view:
            self.current_view.bgcolor = self.theme.BG
            self.current_view.padding = self.ui_scale.PAGE_PADDING
            self.current_view.update()

    def change_theme(self, theme_name: str):
        self.theme = Themes.get_theme(theme_name)
        self.settings.color_theme = theme_name.lower()
        self.update()

    def change_ui_scale(self, ui_scale: str):
        self.ui_scale = UIScales.get_ui_scale(ui_scale)
        self.settings.ui_scale = ui_scale.lower()
        self.update()


class MissingKeys(Enum):
    NONE = "none"
    SOME = "some"
    ALL = "all"

