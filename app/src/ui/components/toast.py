import flet as ft
from typing import Optional

from configs import ThemeManager

def show_toast(
        message: str,
        toast_type: str = None,
        theme_manager: Optional[ThemeManager] = None
        ):
    text_color = {
        "danger": theme_manager.theme.DANGER,
        "warning": theme_manager.theme.WARNING,
        "success": theme_manager.theme.SUCCESS,
        "info": theme_manager.theme.INFO,
        "normal": theme_manager.theme.TEXT
    }.get(toast_type, "normal")

    theme_manager.settings.page.open(ft.SnackBar(
        bgcolor=theme_manager.theme.BORDER,
        padding=ft.padding.only(top=theme_manager.ui_scale.SEPARATOR_THICKNESS),
        content=ft.Container(
            ft.Text(
                value=message,
                color=text_color,
                size=theme_manager.ui_scale.FONTSIZE.NAME
            ),
            bgcolor=theme_manager.theme.BG_LIGHT,
            padding=theme_manager.ui_scale.GENERAL_SPACING
        )
    ))
    theme_manager.settings.page.update()
