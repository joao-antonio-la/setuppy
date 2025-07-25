import flet as ft

from typing import Optional, Union, Callable
from configs import ThemeManager

from .base import BaseComponent
from .colored_button import ColoredButton


class ErrorCard(ft.AlertDialog, BaseComponent):
    def __init__(
        self,
        content: Union[str, ft.Control],
        theme_manager: ThemeManager,
        on_close: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(modal=True, title=ft.Text("Error"), **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self)

        self.theme_manager = theme_manager
        self.on_close = on_close

        self.content = ft.Text(content, color=theme_manager.theme.INFO) if isinstance(content, str) else content
            
        self.actions = [
            ColoredButton(
                text="Continue",
                events={
                    "on_click": lambda _: self.close_card()
                },
                theme_manager=theme_manager
            )
        ]
        self.actions_alignment = ft.MainAxisAlignment.END

    def show(self):
        self.theme_manager.settings.page.open(self)

    def close_card(self):
        self.theme_manager.settings.page.close(self)
        if self.on_close:
            self.on_close()
