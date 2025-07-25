import flet as ft
from typing import Union

from ui.components import Components
from configs import ThemeManager, Settings
from core import play_sound, SOUND_TYPE, enable_startup, disable_startup


def SettingsView(
        page: ft.Page,
        theme_manager: ThemeManager,
        settings: Settings,
        components: Components
    ):

    settings_copy = settings.to_dict()

    def save_and_return():
        try:
            settings.set_settings(settings_copy)
            settings.save_settings()
            components.show_toast(
                message="Settings saved!",
                toast_type="success"
            )
            play_sound(SOUND_TYPE.SUCCESS)
        except Exception as e:
            components.show_toast(
                message="Coulnd't save the settings.\n" + str(e),
                toast_type="danger"
            )
            play_sound(SOUND_TYPE.ERROR)
        page.go("/")

    def set_setting_on_copy(key: str, value: Union[str, int, float, bool]):
        settings_copy[key] = value.strip() if isinstance(value, str) else value
    
    view = ft.View(
        route="/settings",
        controls=[
            ft.Row(
                controls=[
                    components.PageHeader("Settings"),
                    ft.Row(
                        controls=[
                            components.ColoredButton(
                                text="Return",
                                icon=ft.Icons.ARROW_BACK,
                                events={
                                    "on_click": lambda _: save_and_return(),
                                    
                                }
                            )
                        ],
                        spacing=theme_manager.ui_scale.GENERAL_SPACING
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            components.Separator(),
            ft.Column(
                controls=[
                    components.ThemeSelector(
                        value=settings.color_theme,
                        label="Color theme",
                        data="ColorTheme",
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    ),
                    components.Switch(
                        value=settings.launch_on_system_boot,
                        label="Launch app on system boot",
                        data="LaunchOnSystemBoot",
                        events={
                            "on_change": [
                                lambda e: enable_startup() if e.control.value else disable_startup(),
                                lambda e: set_setting_on_copy(e.control.data, e.control.value)
                            ] 
                        }
                    ),
                    components.Switch(
                        value=settings.show_steps_output,
                        label="Show steps output",
                        data="ShowStepsOutput",
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    ),
                    components.Switch(
                        value=settings.system_notifications,
                        label="System notifications",
                        data="SystemNotifications",
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    ),
                    components.Switch(
                        value=settings.sound_alerts,
                        label="Sound alerts",
                        data="SoundAlerts",
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    ),
                    components.ButtonRadioGroup(
                        value=settings.ui_scale,
                        label="User interface scale",
                        data="UIScale",
                        options={
                            "Small": "small",
                            "Normal": "normal",
                            "Big": "big"
                        },
                        events={
                            "on_change": [
                                lambda e: theme_manager.change_ui_scale(e.control.value),
                                lambda e: set_setting_on_copy(e.control.data, e.control.value)
                            ],
                        }
                    ),
                    components.ButtonRadioGroup(
                        value=settings.error_handling_strategy,
                        label="Error handling strategy",
                        data="ErrorHandlingStrategy",
                        options={
                            "Stop": "stop",
                            "Continue": "continue"
                        },
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    ),
                    components.TextInput(
                        value=settings.steps_interval,
                        label="Time interval between steps (miliseconds)",
                        data="StepsInterval",
                        only_numbers=True,
                        std_value=0,
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, int(e.control.value))
                        }
                    ),
                    components.FilePathInput(
                        value=settings.default_setups_file,
                        label="Default setups file",
                        data="DefaultSetupsFile",
                        std_value=settings.std_settings.get("DefaultSetupsFile"),
                        events={
                            "on_change": lambda e: set_setting_on_copy(e.control.data, e.control.value)
                        }
                    )
                ],
                spacing=theme_manager.ui_scale.GENERAL_SPACING,
                expand=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        ]
    )
    theme_manager.set_current_view(view)
    return view

