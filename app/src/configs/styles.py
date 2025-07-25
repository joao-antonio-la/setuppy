import flet as ft
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    BG_DARK: str
    BG: str
    BG_LIGHT: str
    TEXT: str
    TEXT_MUTED: str
    HIGHLIGHT: str
    BORDER: str
    BORDER_MUTED: str
    PRIMARY: str
    SECONDARY: str
    DANGER: str
    WARNING: str
    SUCCESS: str
    INFO: str


class Themes:
    GREEN = Theme(
        BG_DARK="#030303",
        BG="#0A0A0A",
        BG_LIGHT="#171717",
        TEXT="#F2F2F2",
        TEXT_MUTED="#B0B0B0",
        HIGHLIGHT="#636363",
        BORDER="#474747",
        BORDER_MUTED="#2E2E2E",
        PRIMARY="#2A8C34",
        SECONDARY="#6EB876",
        DANGER="#BB928B",
        WARNING="#A6A17D",
        SUCCESS="#85A894",
        INFO="#8DA0BF"
    )

    PURPLE = Theme(
        BG_DARK="#030303",
        BG="#0A0A0A",
        BG_LIGHT="#171717",
        TEXT="#F2F2F2",
        TEXT_MUTED="#B0B0B0",
        HIGHLIGHT="#636363",
        BORDER="#474747",
        BORDER_MUTED="#2E2E2E",
        PRIMARY="#7137B8",
        SECONDARY="#B289E4",
        DANGER="#BB928B",
        WARNING="#A6A17D",
        SUCCESS="#85A894",
        INFO="#8DA0BF"
    )

    YELLOW = Theme(
        BG_DARK="#030303",
        BG="#0A0A0A",
        BG_LIGHT="#171717",
        TEXT="#F2F2F2",
        TEXT_MUTED="#B0B0B0",
        HIGHLIGHT="#636363",
        BORDER="#474747",
        BORDER_MUTED="#2E2E2E",
        PRIMARY="#B8A937",
        SECONDARY="#E4D989",
        DANGER="#BB928B",
        WARNING="#A6A17D",
        SUCCESS="#85A894",
        INFO="#8DA0BF"
    )
    
    GREEN_LIGHT = Theme(
        BG_DARK="#DDDDDD",
        BG="#E6E6E6",
        BG_LIGHT="#FFFFFF",
        TEXT="#0A0A0A",
        TEXT_MUTED="#474747",
        HIGHLIGHT="#FFFFFF",
        BORDER="#808080",
        BORDER_MUTED="#9E9E9E",
        PRIMARY="#2A8C34",
        SECONDARY="#6EB876",
        DANGER="#7F5953",
        WARNING="#6B6543",
        SUCCESS="#4A6D5A",
        INFO="#526380"
    )

    themes: dict[str, Theme] = {
        "green": GREEN,
        "purple": PURPLE,
        "yellow": YELLOW,
        "green light": GREEN_LIGHT,
    }

    @staticmethod
    def get_theme(theme_name: str) -> Theme:
        return Themes.themes.get(theme_name.lower(), Themes.GREEN)


@dataclass(frozen=True)
class FontSize:
    HEADER: int
    CONTAINER_LABEL: int
    NAME: int
    BUTTON: int
    TERMINAL: int


class FontSizes:
    SMALL = FontSize(
        HEADER=20,
        CONTAINER_LABEL=16,
        NAME=14,
        BUTTON=14,
        TERMINAL=13
    )

    NORMAL = FontSize(
        HEADER=26,
        CONTAINER_LABEL=20,
        NAME=18,
        BUTTON=18,
        TERMINAL=16
    )

    BIG = FontSize(
        HEADER=34,
        CONTAINER_LABEL=26,
        NAME=22,
        BUTTON=22,
        TERMINAL=20
    )

    sizes: dict[str, FontSize] = {
        "small": SMALL,
        "normal": NORMAL,
        "big": BIG
    }

    @staticmethod
    def get_font_size(font_size: str) -> FontSize:
        return FontSizes.sizes.get(font_size.lower(), FontSizes.NORMAL)

@dataclass(frozen=True)
class UIScale:
    FONTSIZE: FontSize
    SEPARATOR_THICKNESS: float
    BORDER_THICKNESS: float
    BTN_HEIGHT: float
    BTN_TEXT_WEIGHT: float
    BTN_PADDING: ft.Padding
    TXT_IPT_PADDING: ft.Padding
    PAGE_PADDING: ft.Padding
    GENERAL_SPACING: float
    BORDER_RADIUS: float
    THEME_OPTION_WIDTH: float
    
class UIScales:
    SMALL = UIScale(
        FONTSIZE=FontSizes.get_font_size("small"),
        SEPARATOR_THICKNESS=1.5,
        BORDER_THICKNESS=1.5,
        BTN_HEIGHT=40,
        BTN_TEXT_WEIGHT=ft.FontWeight.W_600,
        BTN_PADDING=ft.padding.symmetric(vertical=0, horizontal=12),
        TXT_IPT_PADDING=ft.padding.symmetric(vertical=8, horizontal=12),
        PAGE_PADDING=ft.padding.all(30),
        GENERAL_SPACING=12,
        BORDER_RADIUS=10,
        THEME_OPTION_WIDTH=80
    )

    NORMAL = UIScale(
        FONTSIZE=FontSizes.get_font_size("normal"),
        SEPARATOR_THICKNESS=2,
        BORDER_THICKNESS=2,
        BTN_HEIGHT=50,
        BTN_TEXT_WEIGHT=ft.FontWeight.W_700,
        BTN_PADDING=ft.padding.symmetric(horizontal=16),
        TXT_IPT_PADDING=ft.padding.symmetric(vertical=12, horizontal=16),
        PAGE_PADDING=ft.padding.all(30),
        GENERAL_SPACING=16,
        BORDER_RADIUS=12.5,
        THEME_OPTION_WIDTH=100
    )

    BIG = UIScale(
        FONTSIZE=FontSizes.get_font_size("big"),
        SEPARATOR_THICKNESS=3,
        BORDER_THICKNESS=3,
        BTN_HEIGHT=60,
        BTN_TEXT_WEIGHT=ft.FontWeight.W_800,
        BTN_PADDING=ft.padding.symmetric(horizontal=20),
        TXT_IPT_PADDING=ft.padding.symmetric(vertical=16, horizontal=20),
        PAGE_PADDING=ft.padding.all(30),
        GENERAL_SPACING=20,
        BORDER_RADIUS=15,
        THEME_OPTION_WIDTH=120
    )

    sizes: dict[str, UIScale] = {
        "small": SMALL,
        "normal": NORMAL,
        "big": BIG
    }

    @staticmethod
    def get_ui_scale(ui_scale: str) -> UIScale:
        return UIScales.sizes.get(ui_scale.lower(), UIScales.SMALL)
    