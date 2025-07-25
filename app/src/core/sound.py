from playsound import playsound
from enum import Enum
import threading
import os

from configs import Paths


class SOUND_TYPE(Enum):
    ERROR = os.path.join(Paths.ASSETS_DIR, "sounds", "error.wav")
    SUCCESS = os.path.join(Paths.ASSETS_DIR, "sounds", "success.wav")
    HINT = os.path.join(Paths.ASSETS_DIR, "sounds", "hint.wav")

def play_sound(path: str | SOUND_TYPE):
    if isinstance(path, SOUND_TYPE):
        path = path.value

    if os.path.exists(path):
        threading.Thread(target=playsound, args=(path,), daemon=True).start()
