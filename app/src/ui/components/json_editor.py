import flet as ft
import json

from typing import Optional, Union, Dict, List, Callable, Any
from configs import ThemeManager
from core import play_sound, SOUND_TYPE

from .base import BaseComponent
from .toast import show_toast


class JsonEditor(ft.TextField, BaseComponent):
    def __init__(
        self,
        value: Optional[Dict] = None,
        data: Any = None,
        events: Optional[Dict[str, List[Callable]]] = None,
        shortcuts: Dict[str, Union[str, Callable]] = {},
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(value=json.dumps(value, indent=4), data=data, multiline=True, expand=True, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self, events=events)

        self.shortcuts = shortcuts
        
        theme_manager.settings.page.on_keyboard_event = self.handle_keypress
        
        self.theme_manager = theme_manager
        self.page = theme_manager.settings.page
        self.value = json.dumps(value, indent=4)
        self.apply_theme(theme_manager)

    def handle_keypress(self, e: ft.KeyboardEvent) -> None:
        if e.data in self.shortcuts:
            executable = self.shortcuts[e.data]
            if isinstance(executable, str):
                method = getattr(self, executable, None)
                if callable(method):
                    method()
            elif callable(executable):
                executable()
                
    def insert_new(self) -> None:
        try:
            parsed = json.loads(self.value)
        except Exception as e:
            show_toast(
                "Invalid JSON, cannot insert new object:" + str(e),
                "danger",
                self.theme_manager
            )
            if self.theme_manager.settings.sound_alerts:
                play_sound(SOUND_TYPE.ERROR)
            return

        new_setup = {
            "New Setup": [
                "echo \"command\""
            ]
        }

        if isinstance(parsed, dict):
            parsed.update(new_setup)
        else:
            show_toast(
                "JSON is not a dict, can't insert",
                "danger",
                self.theme_manager
            )
            if self.theme_manager.settings.sound_alerts:
                play_sound(SOUND_TYPE.ERROR)
            return

        self.value = json.dumps(parsed, indent=4)
        self.update()

    def is_valid(self) -> bool:
        try:
            parsed = json.loads(self.value)
        except Exception as e:
            show_toast(
                "Invalid JSON format: " + str(e),
                "danger",
                self.theme_manager
            )
            if self.theme_manager.settings.sound_alerts:
                play_sound(SOUND_TYPE.ERROR)
            return False
        
        if not isinstance(parsed, dict):
            show_toast(
                "Invalid JSON format: The whole file must be contained within an object",
                "danger",
                self.theme_manager
            )
            if self.theme_manager.settings.sound_alerts:
                play_sound(SOUND_TYPE.ERROR)
            return False
        
        for setup_name, setup_steps in parsed.items():
            if not isinstance(setup_steps, list) or not all(isinstance(step, str) for step in setup_steps):
                show_toast(
                    "Invalid JSON format: The steps of a setup must be a list of strings",
                    "danger",
                    self.theme_manager
                )
                if self.theme_manager.settings.sound_alerts:
                    play_sound(SOUND_TYPE.ERROR)
                return False
            if len(setup_steps) == 0:
                show_toast(
                    f"Setup \"{setup_name}\" has an empty list of steps.",
                    "danger",
                    self.theme_manager
                )
                if self.theme_manager.settings.sound_alerts:
                    play_sound(SOUND_TYPE.ERROR)
                return False
            
        return True
        
    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        self.color = theme_manager.theme.TEXT
        self.border_color = theme_manager.theme.BORDER
        self.border_width = theme_manager.ui_scale.BORDER_THICKNESS
        self.border_radius = theme_manager.ui_scale.BORDER_RADIUS
        self.content_padding = theme_manager.ui_scale.TXT_IPT_PADDING
        self.text_size = theme_manager.ui_scale.FONTSIZE.NAME
        self.label_style = ft.TextStyle(
            size=theme_manager.ui_scale.FONTSIZE.NAME,
            color=theme_manager.theme.SECONDARY
        )

