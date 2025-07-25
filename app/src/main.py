import flet as ft

from configs import ThemeManager, Settings, Paths
from core import SetupsLoader, notify, get_icon, play_sound, SOUND_TYPE

from ui.components import Components
import ui.views as views


def main(page: ft.Page):
    settings = Settings(page)
    theme_manager = ThemeManager(settings)
    components = Components(theme_manager)
    setups_loader = SetupsLoader(settings)
    
    page.title = "Setuppy"
    page.window.icon = get_icon()

    def route_change(route):
        page.views.clear()
        if page.route == "/":
            page.views.append(views.MainView(page, theme_manager, settings, components, setups_loader))
        elif page.route == "/settings":
            page.views.append(views.SettingsView(page, theme_manager, settings, components))
        elif page.route == "/setups_file":
            page.views.append(views.SetupsFileView(page, theme_manager, settings, components, setups_loader))

        page.update()
        
    page.on_route_change = route_change
    page.go("/")

    def show_errors_queue(errors: list[str]):
        def show_next():
            if not errors:
                return
            
            error_msg = errors.pop(0)

            error_card = components.ErrorCard(
                content=error_msg,
                on_close=show_next
            )
            error_card.show()

        show_next()

    if settings.system_notifications:
        notify("App Running", "Setuppy is currently running.", settings)

    if settings.loading_errors:
        if settings.sound_alerts:
            play_sound(SOUND_TYPE.ERROR)
        show_errors_queue(settings.loading_errors.copy())


ft.app(target=main, assets_dir=Paths.ASSETS_DIR)