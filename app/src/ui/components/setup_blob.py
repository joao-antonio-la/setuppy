import flet as ft

from typing import Optional, Any, Union, Dict, List, Callable
from configs import ThemeManager
from core import SetupsLoader, SetupRunner

from .base import BaseComponent


class SetupBlob(ft.Container, BaseComponent):
    def __init__(
        self,
        loader: SetupsLoader,
        runner: SetupRunner,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self)

        def delete_setup_helper():
            loader.delete_setup(runner.setup)
            self.parent.controls.remove(self)
            self.parent.update()

        self.blob_name = ft.Text(runner.setup.name)
        
        self.play_button = ft.IconButton(ft.Icons.PLAY_ARROW, on_click=lambda _: runner.start())
        self.stop_button = ft.IconButton(ft.Icons.STOP, on_click=lambda _: runner.stop())
        self.delete_button = ft.IconButton(ft.Icons.DELETE, on_click=lambda _: delete_setup_helper())

        self.actions_row = ft.Row(
            controls=[self.play_button, self.stop_button, self.delete_button]
        )

        self.content = ft.Row(
            controls=[
                self.blob_name,
                self.actions_row
            ],
            expand=True,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        self.apply_theme(theme_manager)

    def get_controls_to_disable(self) -> List[ft.Control]:
        return [self.play_button, self.delete_button]

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        
        self.blob_name.color = theme_manager.theme.TEXT
        self.blob_name.size = theme_manager.ui_scale.FONTSIZE.NAME

        self.actions_row.spacing = 0
        for button in self.actions_row.controls:
            button.icon_color = theme_manager.theme.TEXT
            button.icon_size = theme_manager.ui_scale.BTN_HEIGHT / 2

        self.bgcolor = theme_manager.theme.BG_LIGHT
        self.border_radius = theme_manager.ui_scale.BORDER_RADIUS
        self.border = ft.border.all(
            width=theme_manager.ui_scale.BORDER_THICKNESS,
            color=theme_manager.theme.BORDER
        )
        self.padding = theme_manager.ui_scale.BTN_PADDING