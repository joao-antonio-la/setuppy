import flet as ft

from typing import Optional, Any, Union, Dict, List, Callable
from configs import ThemeManager

from .base import BaseComponent
from .plain_button import PlainButton


class ButtonRadioGroup(ft.Column, BaseComponent):
    def __init__(
        self,
        value: Any = None,
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        options: Optional[Dict[str, Any]] = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(data=data, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.label: ft.Container = ft.Container(
            content=label if isinstance(label, ft.Control) else ft.Text(value=label)
        )

        self.options_row = ft.Row(
            controls=[
                PlainButton(
                    text=option_name,
                    icon=None,
                    data=option_value,
                    theme_manager=theme_manager,
                    opacity=1.0 if option_value == value else 0.3,
                    events={
                        "on_click": [
                            lambda e: self.select_option(e),
                        ],
                    }
                ) for option_name, option_value in options.items()
            ]
        )

        self.controls = [self.label, self.options_row]

        self.apply_theme(theme_manager)

    def select_option(self, e: ft.ControlEvent):
        value = e.control.data
        for option in self.options_row.controls:
            if option.data == value:
                option.opacity = 1.0
                self.value = value
                if hasattr(self, "on_change"):
                    e.control = self
                    self.on_change(e)
            else: 
                option.opacity = 0.3
            option.update()

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        
        self.spacing = theme_manager.ui_scale.GENERAL_SPACING
        
        label_content = self.label.content
        if isinstance(label_content, ft.Text):
            label_content.size = theme_manager.ui_scale.FONTSIZE.NAME
            label_content.color = theme_manager.theme.TEXT
        
        self.options_row.spacing = theme_manager.ui_scale.GENERAL_SPACING
