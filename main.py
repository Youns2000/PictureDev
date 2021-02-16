import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
import time

def print_sound(indata, outdata, frames, times, status):
    volume_norm = np.linalg.norm(indata)*10
    # print ("|" * int(volume_norm))
    # all.append(int(volume_norm))
    if(int(volume_norm)>180):
        keyboard.press_and_release('alt+tab')

if __name__ == "__main__":
    with sd.Stream(callback=print_sound):
        input('Press ENTER to stop...\n')