import platform
import os


def enable_startup():
    system = platform.system()
    if system == "Windows":
        enable_startup_windows()
    elif system == "Darwin":
        enable_startup_macos()
    elif system == "Linux":
        enable_startup_linux()

def disable_startup():
    system = platform.system()
    if system == "Windows":
        disable_startup_windows()
    elif system == "Darwin":
        disable_startup_macos()
    elif system == "Linux":
        disable_startup_linux()

def enable_startup_windows():
    startup_path = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    script_path = os.path.abspath("setuppy.pyw")
    shortcut_path = os.path.join(startup_path, "Setuppy.lnk")

    if not os.path.exists(script_path):
        return

    import win32com.client
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = script_path
    shortcut.WorkingDirectory = os.path.dirname(script_path)
    shortcut.IconLocation = script_path
    shortcut.save()

def disable_startup_windows():
    startup_path = os.path.join(os.getenv("APPDATA"), r"Microsoft\Windows\Start Menu\Programs\Startup")
    shortcut_path = os.path.join(startup_path, "Setuppy.lnk")
    if os.path.exists(shortcut_path):
        os.remove(shortcut_path)

def enable_startup_macos():
    script_path = os.path.abspath("setuppy.py")
    plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.joao.setuppy</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>{script_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>"""

    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.joao.setuppy.plist")
    with open(plist_path, "w") as f:
        f.write(plist_content)


def disable_startup_macos():
    plist_path = os.path.expanduser("~/Library/LaunchAgents/com.joao.setuppy.plist")
    if os.path.exists(plist_path):
        os.remove(plist_path)        

def enable_startup_linux():
    autostart_path = os.path.expanduser("~/.config/autostart")
    os.makedirs(autostart_path, exist_ok=True)

    script_path = os.path.abspath("setuppy.py")

    desktop_entry = f"""[Desktop Entry]
Type=Application
Exec=python3 {script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Setuppy
Comment=Launch Setuppy on startup
"""

    with open(os.path.join(autostart_path, "setuppy.desktop"), "w") as f:
        f.write(desktop_entry)


def disable_startup_linux():
    autostart_file = os.path.expanduser("~/.config/autostart/setuppy.desktop")
    if os.path.exists(autostart_file):
        os.remove(autostart_file)