import flet as ft

from typing import Optional, Union, Dict, List, Callable, Any
from configs import ThemeManager

from .base import BaseComponent


class TextInput(ft.TextField, BaseComponent):
    def __init__(
        self,
        value: Union[str, int, float] = "",
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        only_numbers: bool = False,
        std_value: Union[str, int, float] = "",
        auto_strip: bool = True,
        events: Optional[Dict[str, List[Callable]]] = None,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(value=str(value), label=label, data=data, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.std_value = str(std_value)

        if only_numbers:
            self.input_filter = ft.NumbersOnlyInputFilter()

        self.add_event_handler("on_blur", self._handle_on_blur)

        if auto_strip:
            self.add_event_handler("on_change", self._handle_on_change)

        self.apply_theme(theme_manager)

    def _handle_on_blur(self, e: ft.ControlEvent) -> None:
        if not str(self.value).strip():
            self.value = self.std_value
            self.update()

    def _handle_on_change(self, e: ft.ControlEvent) -> None:
        new_value = str(self.value).strip()
        if new_value != self.value:
            self.value = new_value
            self.update()

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.color = theme_manager.theme.TEXT
        self.border_color = theme_manager.theme.BORDER
        self.border_width = theme_manager.ui_scale.BORDER_THICKNESS
        self.height = theme_manager.ui_scale.BTN_HEIGHT
        self.border_radius = theme_manager.ui_scale.BORDER_RADIUS
        self.content_padding = theme_manager.ui_scale.TXT_IPT_PADDING
        self.text_size = theme_manager.ui_scale.FONTSIZE.NAME
        self.label_style = ft.TextStyle(
            size=theme_manager.ui_scale.FONTSIZE.NAME,
            color=theme_manager.theme.SECONDARY
        )