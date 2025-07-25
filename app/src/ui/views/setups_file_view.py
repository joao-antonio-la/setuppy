import json
import flet as ft

from ui.components import Components
from configs import ThemeManager, Settings
from core import SetupsLoader, play_sound, SOUND_TYPE


def SetupsFileView(
        page: ft.Page,
        theme_manager: ThemeManager,
        settings: Settings,
        components: Components,
        setups_loader: SetupsLoader,
        **kwargs
    ):

    def return_to_main():
        page.go("/")

    def save_changes():
        if json_editor.is_valid():
            setups_loader.setups_dict = json.loads(json_editor.value)
            setups_loader.save_setups()
            components.show_toast(
                message="Setups saved!"
            )
            play_sound(SOUND_TYPE.SUCCESS)
            save_button.set_disabled()

    save_button = components.ColoredButton(
        text="Save",
        icon=ft.Icons.SAVE,
        disabled=True,
        events={
            "on_click": lambda _: save_changes(),
        }
    )

    json_editor = components.JsonEditor(
        value=setups_loader.setups_dict,
        events={
            "on_change": lambda _: save_button.set_enabled()
        },
        shortcuts={
            '{"key":"S","shift":false,"ctrl":true,"alt":false,"meta":false}': lambda: save_changes(),
            '{"key":"N","shift":false,"ctrl":true,"alt":false,"meta":false}': "insert_new",
            '{"key":"K","shift":false,"ctrl":true,"alt":false,"meta":false}': "clean_value"
        }
    )

    view = ft.View(
        route="/setups_file",
        controls=[
            ft.Row(
                controls=[
                    components.PageHeader("Setups File"),
                    ft.Row(
                        controls=[
                            components.ColoredButton(
                                text="Return",
                                icon=ft.Icons.ARROW_BACK,
                                events={
                                    "on_click": lambda _: return_to_main(),
                                    
                                }
                            ),
                            save_button
                        ],
                        spacing=theme_manager.ui_scale.GENERAL_SPACING
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            components.Separator(),
            ft.Column(
                controls=[
                    ft.Container(
                        content=json_editor,
                        expand=True
                    ),
                    ft.Column(
                        controls=[
                            components.SmallLabel("Ctrl + S or Save Button: Save the contents."),
                            components.SmallLabel("Ctrl + N: Insert a new standard setup."),
                        ],
                        spacing=0
                    )
                ],
                expand=True
            )
        ]
    )
    
    theme_manager.set_current_view(view)
    return view
