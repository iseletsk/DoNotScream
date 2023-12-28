import sounddevice as sd
import numpy as np
import subprocess
import sys
import time

SCREAM_VOLUME=10


class ScreamDetector:
    def __init__(self):
        self.counter = 10
        self.last_scream = time.time()
        pass



    def show_banner(self, dont_repeat_seconds=5):
        current_time = time.time()
        if current_time - self.last_scream > dont_repeat_seconds:
            self.last_scream = current_time
            ScreamDetector._show_banner()

    @staticmethod
    def _show_banner():
        subprocess.run(["osascript", "-e", 'display dialog "\nYOU ARE SCREAMING\n\n" buttons {"OK"} giving up after 1'])

    def test_sound(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        if volume_norm > SCREAM_VOLUME:
            self.counter += 1
            #print("Scream detected", self.counter)
            if self.counter > 20:
                self.show_banner()

    def decrease_counter(self):
        if self.counter > 0:
            self.counter -= 1



if __name__ == "__main__":
    if len(sys.argv) > 1:
        SCREAM_VOLUME = int(sys.argv[1])
    scream_detector = ScreamDetector()
    with sd.InputStream(callback=scream_detector.test_sound):
        while True:
            sd.sleep(100)
            scream_detector.decrease_counter()

