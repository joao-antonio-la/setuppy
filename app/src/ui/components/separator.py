import flet as ft

from typing import Optional
from configs import ThemeManager

from .base import BaseComponent


class Separator(ft.Divider, BaseComponent):
    def __init__(
        self,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(**kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self)

        self.apply_theme(theme_manager)

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.color = theme_manager.theme.PRIMARY
        self.thickness = theme_manager.ui_scale.SEPARATOR_THICKNESS