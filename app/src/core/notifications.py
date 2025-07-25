import os
import platform
from plyer import notification

from configs import Settings, Paths


def get_icon() -> str:
    system = platform.system()
    if system == "Windows":
        return os.path.join(Paths.ASSETS_DIR, "icons", "icon.ico")
    return os.path.join(Paths.ASSETS_DIR, "icons", "icon.png")

def notify(title: str, message: str, settings: Settings):
    if not settings.system_notifications:
        return

    notification.notify(
        title=title,
        message=message,
        app_name="Setuppy",
        app_icon=get_icon(),
        timeout=3
    )