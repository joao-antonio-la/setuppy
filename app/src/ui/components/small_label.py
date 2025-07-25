import flet as ft

from typing import Optional
from configs import ThemeManager

from .base import BaseComponent


class SmallLabel(ft.Text, BaseComponent):
    def __init__(
        self,
        value: str = "",
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(value=value, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self)

        self.apply_theme(theme_manager)

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.color = theme_manager.theme.TEXT_MUTED
        self.size = theme_manager.ui_scale.FONTSIZE.TERMINAL