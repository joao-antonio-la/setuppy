import flet as ft

from ui.components import Components

from configs import ThemeManager, Settings
from core import SetupsLoader, SetupRunner


def MainView(
        page: ft.Page,
        theme_manager: ThemeManager,
        settings: Settings,
        components: Components,
        setups_loader: SetupsLoader
    ):

    all_controls_to_manage = []

    setups_button = components.ColoredButton(
        text="Setups",
        icon=ft.Icons.CODE,
        events={"on_click": lambda _: page.go("/setups_file")}
    )
    settings_button = components.ColoredIconButton(
        icon=ft.Icons.SETTINGS,
        events={"on_click": lambda _: page.go("/settings")}
    )

    all_controls_to_manage.extend([setups_button, settings_button])
    output_box = components.OutputBox() if settings.show_steps_output else None
    blobs_column = ft.Column(scroll="auto", expand=True)
    runners_buffer = []

    for setup in setups_loader.setups:
        runner = SetupRunner(
            setup=setup,
            settings=settings,
            log_callback=output_box.log_line,
            log_start_callback=output_box.log_start,
            log_end_callback=output_box.log_end,
            log_stop_callback=output_box.log_stop
        ) if output_box else SetupRunner(
            setup=setup,
            settings=settings
        )

        runners_buffer.append(runner)
    
        blob = components.SetupBlob(
            loader=setups_loader,   
            runner=runner,
        )

        blobs_column.controls.append(blob)
        all_controls_to_manage.extend(blob.get_controls_to_disable())

    for runner in runners_buffer:
        runner.controls_to_disable = all_controls_to_manage + blob.get_controls_to_disable()

    view = ft.View(
        route="/",
        controls=[
            ft.Row(
                controls=[
                    components.PageHeader(value="Your Setups"),
                    ft.Row(
                        controls=[setups_button, settings_button],
                        spacing=theme_manager.ui_scale.GENERAL_SPACING
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            components.Separator(),
            blobs_column
        ]
    )

    if settings.show_steps_output:
        view.controls.append(
            ft.Row(
                controls=[
                    ft.Container(
                        content=output_box,
                        expand=True
                    )
                ]
            )
        )
    
    theme_manager.set_current_view(view)
    return view
