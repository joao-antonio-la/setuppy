import threading
import time
import subprocess
import flet as ft

from typing import Optional, Callable, List

from .setup import Setup
from .notifications import notify
from .sound import play_sound, SOUND_TYPE
from configs import Settings


class SetupRunner:
    def __init__(
        self,
        setup: Setup,
        settings: Settings,
        log_callback: Optional[Callable[[str, str, bool, Optional[str]], None]] = None,
        log_start_callback: Optional[Callable[[str], None]] = None,
        log_end_callback: Optional[Callable] = None,
        log_stop_callback: Optional[Callable] = None,
        controls_to_disable: Optional[List[ft.Control]] = []
    ):
        self.setup = setup
        self.settings = settings
        self.log_callback = log_callback
        self.log_start_callback = log_start_callback
        self.log_end_callback = log_end_callback
        self.log_stop_callback = log_stop_callback
        self.controls_to_disable = controls_to_disable

        self._thread: threading.Thread = None
        self._stop_event: threading.Event = threading.Event()

    def start(self):
        if self._thread and self._thread.is_alive():
            return

        self._stop_event.clear()
        self._thread = threading.Thread(target=self._run)

        for control in self.controls_to_disable:
            control.disabled = True
            control.opacity = 0.3
            control.update()

        self._thread.start()

    def _run(self) -> None:
        stopped_early = False

        if self.log_start_callback:
            if self.settings.sound_alerts:
                play_sound(SOUND_TYPE.HINT)
            self.log_start_callback(self.setup.name)

        for step in self.setup.steps:
            if self._stop_event.is_set():
                stopped_early = True
                break

            time.sleep(self.settings.steps_interval / 1000)

            if self._stop_event.is_set():
                stopped_early = True
                break

            result = self._execute_step(step)

            command = step
            output = result["output"]
            success = result["success"]
            error_message = result["error_message"]

            if self.log_callback:
                if self.settings.sound_alerts:
                    play_sound(SOUND_TYPE.HINT)
                self.log_callback(command, output, success, error_message)

        if stopped_early:
            if self.log_stop_callback:
                if self.settings.sound_alerts:
                    play_sound(SOUND_TYPE.SUCCESS)
                notify("Setup stopped", f"{self.setup.name} was stopped manually.", self.settings)
                self.log_stop_callback()
        else:
            if self.log_end_callback:
                if self.settings.sound_alerts:
                    play_sound(SOUND_TYPE.SUCCESS)
                notify("Setup completed", f"{self.setup.name} finished successfully.", self.settings)
                self.log_end_callback()

        for control in self.controls_to_disable:
            control.disabled = False
            control.opacity = 1
            control.update()
            
    def _execute_step(self, step: str):
        try:
            process = subprocess.Popen(
                step,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True,
                text=True,
            )

            stdout, stderr = process.communicate()

            if stdout:
                return {
                    "success": True,
                    "output": stdout.strip(),
                    "error_message": None
                }
            
            else:
                if self.settings.error_handling_strategy == "stop":
                    self.stop()
                return {
                    "success": False,
                    "output": None,
                    "error_message": stderr.strip()
                }

        except Exception as e:
            if self.settings.error_handling_strategy == "stop":
                self.stop()
            return {
                "success": False,
                "output": None,
                "error_message": str(e)
            }
        
    def stop(self) -> None:
        self._stop_event.set()
        if self._thread and threading.current_thread() != self._thread:
            self._thread.join()