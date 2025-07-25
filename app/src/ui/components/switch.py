import flet as ft

from typing import Callable, Optional, Dict, List, Any, Union
from configs import ThemeManager

from .base import BaseComponent


class Switch(ft.Switch, BaseComponent):
    def __init__(
        self,
        value: bool = False,
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(data=data, value=value, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.label: ft.Container = ft.Container(
            content=label if isinstance(label, ft.Control) else ft.Text(value=label)
        )

        def change_outline_color(e: ft.ControlEvent, theme_manager: ThemeManager):
            control: Switch = e.control
            control.track_outline_color = theme_manager.theme.PRIMARY if control.value else theme_manager.theme.BG_LIGHT
            control.update()

        self.add_event_handler(
            "on_change", lambda e: change_outline_color(e, theme_manager)
        )

        self.apply_theme(theme_manager)

    def apply_theme(self, theme_manager: Optional[ThemeManager]) -> None:
        if not theme_manager:
            return
        
        self.label.margin = ft.margin.only(left=theme_manager.ui_scale.GENERAL_SPACING)
        if isinstance(self.label.content, ft.Text):
            self.label.content.size = theme_manager.ui_scale.FONTSIZE.NAME
            self.label.content.color = theme_manager.theme.TEXT

        self.active_color = theme_manager.theme.PRIMARY
        self.inactive_thumb_color = theme_manager.theme.BG_LIGHT
        self.inactive_track_color = theme_manager.theme.BG_DARK
        self.track_outline_color = theme_manager.theme.PRIMARY if self.value else theme_manager.theme.BG_LIGHT