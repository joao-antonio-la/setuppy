import flet as ft

from typing import Optional, Union, Dict, List, Callable, Any
from configs import ThemeManager

from .base import BaseComponent
from .text_input import TextInput
from .plain_button import PlainButton
from .plain_icon_button import PlainIconButton


class FilePathInput(ft.Row, BaseComponent):
    def __init__(
        self,
        value: Union[str, int, float] = "",
        label: Optional[Union[str, ft.Control]] = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        data: Any = None,
        std_value: Union[str, int, float] = "",
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(data=data, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.value = value
        self.std_value = std_value

        if not hasattr(self, "on_change"):
            self.on_change = lambda _: 1

        self.file_picker = ft.FilePicker(on_result=self._handle_on_change)

        self.text_field = TextInput(
            value=value,
            label=label,
            data=data,
            events={
                "on_change": lambda e: self.on_change(e)
            },
            std_value=std_value,
            theme_manager=theme_manager
        )

        self.browse_btn = PlainButton(
            text="Browse",
            data=data,
            events={
                "on_click": lambda _: self.file_picker.pick_files()
            },
            theme_manager=theme_manager
        )

        theme_manager.settings.page.overlay.append(self.file_picker)
        self.controls = [self.text_field, self.browse_btn]

        if std_value:
            self.controls.append(
                PlainIconButton(
                    icon=ft.Icons.REFRESH,
                    events={
                        "on_click": self._handle_reset
                    },
                    theme_manager=theme_manager
                )
            )

        self.apply_theme(theme_manager)

    def _handle_reset(self, e: ft.ControlEvent):
        self.text_field.value = self.std_value
        self.value = self.std_value
        self.text_field.update()

        if hasattr(self, "_custom_events") and "on_change" in self._custom_events:
            for handler in self._custom_events["on_change"]:
                handler(ft.ControlEvent(target=e.target, name="on_change", control=self, data=self.data, page=self.page))


    def _handle_on_change(self, e: ft.ControlEvent):
        if e.files:
            self.text_field.value = e.files[0].path
            self.text_field.update()

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.text_field.expand = True