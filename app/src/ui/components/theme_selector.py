import flet as ft

from typing import Optional, Union, Any, Dict, List, Callable
from configs import ThemeManager, styles

from .base import BaseComponent


class ThemeSelector(ft.Column, BaseComponent):
    def __init__(
        self,
        value: Optional[str] = None,
        label: Optional[Union[str, ft.Control]] = "",
        data: Any = "",
        events: Optional[Dict[str, List[Callable]]] = None,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.value = value
        self.data = data

        self.label = ft.Container(
            content=ft.Text(value=label) if isinstance(label, str) else label
        )
        self.options_row = ft.Row()

        for theme_name, theme in styles.Themes.themes.items():
            self.options_row.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(bgcolor=theme.PRIMARY),
                            ft.Text(value=theme_name.title(), text_align=ft.TextAlign.CENTER)
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    on_click=lambda e, name=theme_name: self.select_option(e, name, theme_manager)
                )
            )

        self.controls = [self.label, self.options_row]

        self.apply_theme(theme_manager)

    def select_option(self, e: ft.ControlEvent, theme_name: str, theme_manager: ThemeManager):
        self.value = theme_name
        theme_manager.change_theme(theme_name)
        if hasattr(self, "on_change"):
            e.control = self
            self.on_change(e)

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.spacing = theme_manager.ui_scale.GENERAL_SPACING
        self.color = theme_manager.theme.PRIMARY
        self.thickness = theme_manager.ui_scale.SEPARATOR_THICKNESS

        if isinstance(self.label.content, ft.Text):
            self.label.content.size = theme_manager.ui_scale.FONTSIZE.NAME
            self.label.content.style = ft.TextStyle(color=theme_manager.theme.TEXT)
        self.options_row.spacing = theme_manager.ui_scale.GENERAL_SPACING

        option: ft.Container = None
        for option in self.options_row.controls:
            option.width = theme_manager.ui_scale.THEME_OPTION_WIDTH

            column = option.content
            column.spacing = theme_manager.ui_scale.GENERAL_SPACING

            color_container: ft.Container = column.controls[0]
            text: ft.Text = column.controls[1]

            color_container.height = theme_manager.ui_scale.BTN_HEIGHT
            color_container.width = theme_manager.ui_scale.BTN_HEIGHT
            color_container.spacing = theme_manager.ui_scale.GENERAL_SPACING
            color_container.border_radius = theme_manager.ui_scale.BORDER_RADIUS
            color_container.border=ft.border.all(
                width=theme_manager.ui_scale.BORDER_THICKNESS * 2,
                color=theme_manager.theme.TEXT
            ) if self.value == text.value.lower() else None

            text.size = theme_manager.ui_scale.FONTSIZE.NAME
            text.color = theme_manager.theme.TEXT