from re import S
import sounddevice as sd
import numpy as np
import keyboard
import tkinter as tk
from datetime import datetime as dt

class call:
    def __init__(self):
        self.file = "./config.txt"
        # self.file = "/Applications/SoundShutter/config.txt"
        self.last = 0
        self.norm = 0
        self.key = 0 
        self.t = 0
        self.running = False
        self.stream = sd.Stream(callback=self.print_sound)
        ################################################################
        self.window = tk.Tk()
        self.window.title('Sound Shutter')
        self.window.geometry('600x60')
        self.window.iconbitmap('logo.ico') 
        self.run = tk.Button(self.window, text ="Run",  height=30,command = self.run)
        self.config = tk.Button(self.window, text ="Config",  height=30,command = self.config)
        self.stop = tk.Button(self.window, text ="Stop",  height=30, command = self.stop)
        self.label = tk.Label(self.window, text = "")
        self.run.pack(side = "left",fill="x")
        self.config.pack(side = "left",fill="x")
        self.stop.pack(side = "right",fill="x")
        self.label.pack(side = "top")   
        ################################################################


    def print_sound(self,indata, outdata, frames, times, status):
        volume_norm = np.linalg.norm(indata)*10
        vol_str = '|'*(int(volume_norm)//2)
        if(self.running==False):
            raise sd.CallbackStop()
        else:
            if(int(volume_norm)>self.norm and ((float(dt.now().strftime('%S.%f'))-float(self.last))>float(self.t) or float(dt.now().strftime('%S.%f'))<float(self.last))): 
                self.label.config(text=vol_str,fg='#03EF00')
                self.last = int(dt.now().strftime('%S'))
                keyboard.press_and_release(self.key)
            else:
                self.label.config(text=vol_str,fg='#E92904')

    def updateConf(self):
        # fichier = open("/Applications/SoundShutter/config.txt", "r")
        fichier = open(self.file, "r")
        lines = fichier.readlines()
        for l in lines:
            parties = l.split(':')
            parties[0].replace(' ','')
            parties[1].replace('\n','')
            if(parties[0].lower()=="volume"):
                self.norm = int(parties[1])
            elif(parties[0].lower()=="touche"):
                self.key = parties[1].replace('\n','')
            elif(parties[0].lower()=="temps"):
                self.t = float(parties[1])
            else:
                pass
        fichier.close()

    def writeConf(self,norm,key,time):
        fichier = open(self.file, "w+")
        fichier.write("Volume:"+str(norm)+"\nTouche:"+str(key)+"\nTemps:"+str(time))
        fichier.close()

    def run(self):
        self.updateConf()
        self.running = True
        self.stream.start()

    def config(self):
        self.updateConf()
        conf_win = tk.Tk()
        conf_win.title('Configuration')
        conf_win.geometry('330x90')
        conf_win.iconbitmap('logo.ico')

        conf_norm = tk.Label(conf_win, width=20, text = "Norm").grid(row=3, column=0)
        norm_txt = tk.Entry(conf_win)
        norm_txt.insert(0,self.norm)
        norm_txt.grid(row=3, column=1, sticky="ew")

        conf_key = tk.Label(conf_win, width=20, text = "Key").grid(row=4, column=0)
        key_txt = tk.Entry(conf_win)
        key_txt.insert(0,self.key)
        key_txt.grid(row=4, column=1, sticky="ew")
   
        conf_time = tk.Label(conf_win, width=20, text = "Time").grid(row=5, column=0)
        time_txt = tk.Entry(conf_win)
        time_txt.insert(0,self.t)
        time_txt.grid(row=5, column=1, sticky="ew")

        ok = tk.Button(conf_win, text ="OK", command = lambda:[self.writeConf(norm_txt.get(),key_txt.get(),time_txt.get()),conf_win.destroy()]).grid(row=6, column=0, columnspan=2,sticky="SEW")

        conf_win.mainloop()

    def stop(self):
        self.running = False
        self.stream.stop()

if __name__ == "__main__":
    c = call()
    c.window.mainloop()