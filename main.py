import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
import time
from datetime import datetime as dt

class call:
    def __init__(self):
        self.last = 0
    def print_sound(self,indata, outdata, frames, times, status):
        volume_norm = np.linalg.norm(indata)*10
        if(int(volume_norm)>220 and (int(dt.now().strftime('%S'))-self.last)>1): 
            self.last = int(dt.now().strftime('%S'))
            keyboard.press_and_release('space')

if __name__ == "__main__":
    c = call()
    with sd.Stream(callback=c.print_sound):
        input('Press ENTER to stop...\n')