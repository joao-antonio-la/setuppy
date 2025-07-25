import flet as ft

from typing import Callable, Optional, Dict, List, Any
from configs import ThemeManager


class BaseComponent:
    def __init__(
            self,
            theme_manager: Optional[ThemeManager] = None,
            component: Any = None,
            events: Optional[Dict[str, List[Callable]]] = None
        ):
        if theme_manager:
            theme_manager.register(self)

        self._component = component
        self._custom_events = {}
        self._combined_handlers_attached = set()
        if events:
            for event_type, handlers in events.items():
                if not isinstance(handlers, list):
                    handlers = [handlers]
                for handler in handlers:
                    self.add_event_handler(event_type, handler)

    def apply_theme(self, theme_manager: Optional[ThemeManager] = None) -> None:
        # Override this in subclasses to apply theme to internal controls
        pass

    def refresh_theme(self, theme_manager: Optional[ThemeManager]) -> None:
        self.apply_theme(theme_manager)
        if hasattr(self, "update"):
            self.update()

    def add_event_handler(self, event_type: str, handler: Callable):
        handlers = self._custom_events.setdefault(event_type, [])
        handlers.append(handler)
        if event_type not in self._combined_handlers_attached:
            self._attach_combined_handler(event_type)
            self._combined_handlers_attached.add(event_type)

    def _attach_combined_handler(self, event_type: str):
        def combined(e):
            for h in self._custom_events[event_type]:
                h(e)
        setattr(self._component, event_type, combined)
