import flet as ft

from typing import Callable, Optional, Dict, List, Any
from configs import ThemeManager

from .base import BaseComponent

class ColoredButton(ft.ElevatedButton, BaseComponent):
    def __init__(
        self,
        text="",
        icon: ft.IconValue | None = None,
        data: Any = None,
        disabled=False,
        events: Optional[Dict[str, List[Callable]]] = None,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(text=text, icon=icon, data=data, disabled=disabled, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        if "opacity" not in kwargs:
            self.opacity = 0.3 if disabled else 1.0
        self.apply_theme(theme_manager)

    def set_disabled(self) -> None:
        self.disabled = True
        self.opacity = 0.3
        self.update()

    def set_enabled(self) -> None:
        self.disabled = False
        self.opacity = 1.0
        self.update()

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.bgcolor = theme_manager.theme.BG_LIGHT
        self.color = theme_manager.theme.PRIMARY
        self.height = theme_manager.ui_scale.BTN_HEIGHT
        self.style = ft.ButtonStyle(
            side=ft.BorderSide(
                width=theme_manager.ui_scale.BORDER_THICKNESS,
                color=theme_manager.theme.PRIMARY
            ),
            text_style=ft.TextStyle(
                size=theme_manager.ui_scale.FONTSIZE.BUTTON,
                weight=ft.FontWeight.W_600
            ),
            shape=ft.RoundedRectangleBorder(
                radius=theme_manager.ui_scale.BORDER_RADIUS
            ),
            padding=theme_manager.ui_scale.BTN_PADDING,
            overlay_color=ft.Colors.with_opacity(
                color=theme_manager.theme.SECONDARY, opacity=1
            )
        )