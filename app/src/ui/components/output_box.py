import flet as ft

from typing import Optional
from configs import ThemeManager

from .base import BaseComponent


class OutputBox(ft.Container, BaseComponent):
    def __init__(
        self,
        theme_manager: Optional[ThemeManager] = None,
        **kwargs
    ):
        super().__init__(expand=True, **kwargs)
        BaseComponent.__init__(self, theme_manager=theme_manager, component=self)
        
        self.label = ft.Text("Steps Output")
        self.output_lines = ft.Column(expand=True, scroll=ft.ScrollMode.AUTO)

        self.content = ft.Column(
            controls=[
                self.label,
                ft.Row(
                    controls=[
                        self.output_lines
                    ]
                )
            ],
            expand=True
        )

        self.theme_manager = theme_manager
        self.apply_theme(theme_manager)

    def log_line(self, command: str, output: Optional[str] = None, success: bool = True, error_message: Optional[str] = None):
        command_text = ft.Text("> Executing: " + command, color=self.theme_manager.theme.INFO)
        output_text = ft.Text(output or "", color=self.theme_manager.theme.TEXT)
        result_text = ft.Text("Step done with no failures", color=self.theme_manager.theme.SUCCESS) if success else ft.Text("Step failed: " + error_message, color=self.theme_manager.theme.DANGER)

        self.output_lines.controls.append(
            ft.Column(
                controls=[
                    command_text,
                    output_text,
                    result_text
                ],
                expand=True,
                spacing=0
            )
        )
        self.output_lines.scroll_to(-1)
        self.update()

    def log_start(self, setup_name: str):
        self.output_lines.controls.append(
            ft.Column(
                controls=[
                    ft.Text(f"Starting \"{setup_name}\".", color=self.theme_manager.theme.PRIMARY)
                ]
            )
        )
        self.output_lines.scroll_to(-1)
        self.update()

    def log_end(self):
        self.output_lines.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Setup finished.", color=self.theme_manager.theme.PRIMARY)
                ]
            )
        )
        self.output_lines.scroll_to(-1)
        self.update()

    def log_stop(self):
        self.output_lines.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Setup stopped.", color=self.theme_manager.theme.WARNING)
                ]
            )
        )
        self.output_lines.scroll_to(-1)
        self.update()

    def clean_output(self):
        self.output_lines.controls.clear()
        self.update()

    def apply_theme(self, theme_manager: ThemeManager | None) -> None:
        if not theme_manager:
            return
        
        self.padding = theme_manager.ui_scale.GENERAL_SPACING

        self.border = ft.border.all(
            width=theme_manager.ui_scale.BORDER_THICKNESS,
            color=theme_manager.theme.BORDER_MUTED
        )
        self.border_radius = ft.border_radius.all(
            value=theme_manager.ui_scale.BORDER_RADIUS
        )
        self.label.size = theme_manager.ui_scale.FONTSIZE.NAME
        self.label.color = theme_manager.theme.TEXT
        self.output_lines.height = self.theme_manager.ui_scale.FONTSIZE.TERMINAL * 8