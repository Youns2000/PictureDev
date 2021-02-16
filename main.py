import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
import time
from datetime import datetime as dt

class call:
    def __init__(self):
        self.last = 0
        self.norm = 0
        self.key = 0
        self.t = 0

    def print_sound(self,indata, outdata, frames, times, status):
        volume_norm = np.linalg.norm(indata)*10
        if(int(volume_norm)>self.norm and (float(dt.now().strftime('%S.%f'))-float(self.last))>float(self.t)): 
            self.last = int(dt.now().strftime('%S'))
            keyboard.press_and_release(self.key)

if __name__ == "__main__":
    c = call()
    fichier = open("config.txt", "r")
    lines = fichier.readlines()
    for l in lines:
        parties = l.split(':')
        parties[0].replace(' ','')
        parties[1].replace('\n','')
        if(parties[0].lower()=="volume"):
            c.norm = int(parties[1])
        elif(parties[0].lower()=="touche"):
            c.key = parties[1].replace('\n','')
        elif(parties[0].lower()=="temps"):
            c.t = int(parties[1])
        else:
            pass
            

    with sd.Stream(callback=c.print_sound):
        input('Press ENTER to stop...\n')