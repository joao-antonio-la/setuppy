import flet as ft

from typing import Any, Callable, Optional, List, Dict, Union
from configs import ThemeManager
from core import SetupsLoader, SetupRunner

from .base import BaseComponent

from .colored_button import ColoredButton
from .plain_button import PlainButton
from .colored_icon_button import ColoredIconButton
from .plain_icon_button import PlainIconButton
from .page_header import PageHeader
from .small_label import SmallLabel
from .separator import Separator
from .switch import Switch
from .button_radio_group import ButtonRadioGroup
from .text_input import TextInput
from .filepath_input import FilePathInput
from .theme_selector import ThemeSelector
from .json_editor import JsonEditor
from .setup_blob import SetupBlob
from .output_box import OutputBox
from .error_card import ErrorCard
from .toast import show_toast


class Components:
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager

    def ColoredButton(
        self,
        text: str = "",
        icon: Optional[ft.IconValue] = None,
        data: Any = None,
        disabled: bool = False,
        events: dict[str, list[Callable[[ft.ControlEvent], None]]] = None,
        **kwargs
    ) -> ColoredButton:
        return ColoredButton(
            text=text,
            icon=icon,
            data=data,
            disabled=disabled,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def ColoredIconButton(
        self,
        icon: Optional[ft.IconValue] = None,
        data: Any = None,
        disabled: bool = False,
        events: dict[str, list[Callable[[ft.ControlEvent], None]]] = None,
        **kwargs
    ) -> ColoredIconButton:
        return ColoredIconButton(
            icon=icon,
            data=data,
            disabled=disabled,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def PlainButton(
        self,
        text: str = "",
        icon: Optional[ft.IconValue] = None,
        data: Any = None,
        disabled: bool = False,
        events: dict[str, list[Callable[[ft.ControlEvent], None]]] = None,
        **kwargs
    ) -> PlainButton:
        return PlainButton(
            text=text,
            icon=icon,
            data=data,
            disabled=disabled,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def PlainIconButton(
        self,
        icon: Optional[ft.IconValue] = None,
        data: Any = None,
        disabled: bool = False,
        events: dict[str, list[Callable[[ft.ControlEvent], None]]] = None,
        **kwargs
    ) -> PlainIconButton:
        return PlainIconButton(
            icon=icon,
            data=data,
            disabled=disabled,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def PageHeader(
        self,
        value: str = "",
        **kwargs
    ) -> PageHeader:
        return PageHeader(
            value=value,
            theme_manager=self.theme_manager,
            **kwargs
        )

    def SmallLabel(
        self,
        value: str = "",
        **kwargs
    ) -> SmallLabel:
        return SmallLabel(
            value=value,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def Separator(
        self,
        **kwargs
    ) -> Separator:
        return Separator(
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def Switch(
        self,
        value: bool = False,
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        **kwargs
    ) -> Switch:
        return Switch(
            value=value,
            label=label,
            data=data,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        ) 
    
    def ButtonRadioGroup(
        self,
        value: Any = None,
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        options: Dict[str, Any] = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        **kwargs
    ) -> ButtonRadioGroup:
        return ButtonRadioGroup(
            value=value,
            label=label,
            data=data,
            options=options,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def TextInput(
        self,
        value: str = "",
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        only_numbers: bool = False,
        std_value: Union[str, int, float] = "", 
        auto_strip: bool = True,
        events: Optional[Dict[str, List[Callable]]] = None,
        **kwargs
    ) -> TextInput:
        return TextInput(
            value=value,
            label=label,
            data=data,
            only_numbers=only_numbers,
            std_value=std_value,
            auto_strip=auto_strip,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def FilePathInput(
        self,
        value: Union[str, int, float] = "",
        label: Optional[Union[str, ft.Control]] = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        data: Any = None,
        std_value: Union[str, int, float] = "",
        **kwargs
    ) -> FilePathInput:
        return FilePathInput(
            value=value,
            label=label,
            data=data,
            std_value=std_value,
            events=events,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def ThemeSelector(
        self,
        value: Optional[str] = None,
        label: Optional[Union[str, ft.Control]] = "",
        data: Any = "",
        events: Optional[Dict[str, List[Callable]]] = None,
    ) -> ThemeSelector:
        return ThemeSelector(
            value=value,
            label=label,
            data=data,
            events=events,
            theme_manager=self.theme_manager
        )
    
    def JsonEditor(
        self,
        value: Union[str, int, float] = "",
        label: Optional[Union[str, ft.Control]] = None,
        data: Any = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        shortcuts: Dict[str, Union[str, Callable]] = {},
        **kwargs
    ) -> JsonEditor:
        return JsonEditor(
            value=value,
            label=label,
            data=data,
            events=events,
            shortcuts=shortcuts,
            theme_manager=self.theme_manager,
            **kwargs
        )
    
    def SetupBlob(
        self,
        loader: SetupsLoader,
        runner: SetupRunner,
        **kwargs
    ) -> SetupBlob:
        return SetupBlob(
            loader=loader,
            runner=runner,
            theme_manager=self.theme_manager,
            **kwargs
        )

    def OutputBox(
        self,
        **kwargs
    ) -> OutputBox:
        return OutputBox(
            theme_manager=self.theme_manager,
            **kwargs
        )
        
    def ErrorCard(
        self,
        content: Union[str, ft.Control] = None,
        on_close: Optional[Callable[[], None]] = None,
        **kwargs
    ) -> ErrorCard:
        return ErrorCard(
            content=content,
            theme_manager=self.theme_manager,
            on_close=on_close,
            **kwargs
        )
    
    def show_toast(
        self,
        message: str,
        toast_type: str = "normal"
    ) -> None: 
        show_toast(
            message=message,
            toast_type=toast_type,
            theme_manager=self.theme_manager
        )