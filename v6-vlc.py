from threading import Thread
from time import sleep
import tkinter as tk
import ttkbootstrap as ttk

from include.player2 import audioPlayer

root = ttk.Window(themename=["simplex", "vapor", "darkly"][2])
root.title("Music Application")

class songController(ttk.Frame):
    def __init__(self, master):
        ttk.Frame.__init__(self, master)
        self.audio = audioPlayer()
        self.playing = "stopped"
        self.inactive = ttk.Button(self, text="", command=self.playCmd, bootstyle = "success-outline")
        self.active = ttk.Button(self, text="", command=self.playCmd, bootstyle = "success")
        self.current = self.inactive
        self.stop = ttk.Button(self, text="Stop", command=self.stopCmd, state="disabled", bootstyle = "danger-outline", width=5)
        self.previous = ttk.Button(self, text="<", command=self.previousCmd, bootstyle = "warning-outline")
        self.next = ttk.Button(self, text=">", command=self.nextCmd, bootstyle = "warning-outline")
    def playCmd(self):
        self.current = self.active
        if self.playing == "stopped":
            self.playing = "playing"
        elif self.playing == "paused":
            self.playing = "playing"
        else:
            self.playing = "paused"
        self.audio.playToggle()
        self.stop.configure(state="enabled")
        self.packChildren()
    def stopCmd(self):
        self.current = self.inactive
        self.playing = "stopped"
        self.audio.stop()
        self.stop.configure(state="disabled")
        self.packChildren()
    def previousCmd(self):
        print("playing previous song")
    def nextCmd(self):
        print("playing next song")
    def packChildren(self):
        if self.current == self.active:
            self.inactive.grid_forget()
        else:
            self.active.grid_forget()
        if self.playing == "playing":
            self.current.configure(text="Pause")
        else:
            self.current.configure(text="Play")
        self.current.grid(row=0, column=1, sticky="ew")
        self.stop.grid(row=1, column=1, sticky="ew")
        self.previous.grid(row=0, column=0, rowspan=2, sticky="ns")
        self.next.grid(row=0, column=2, rowspan=2, sticky="ns")
class seekerController(ttk.Frame):
    def __init__(self, master, audio : audioPlayer):
        ttk.Frame.__init__(self, master)
        self.seconds = 0
        self.current = 0
        self.slider = ttk.Scale(self, value=0, to=self.seconds)
        self.label = ttk.Label(self, text="(0:00 / 0:00)")
        self.slider.bind("<Button-1>", self.down)
        self.slider.bind("<ButtonRelease-1>", self.up)
        self.updateSlider = True
        self.skipButtons = ttk.Frame(self)
        self.audio = audio
        self.b10 = ttk.Button(self.skipButtons, text="<10- ", command=lambda : self.travel(-10), padding=0, bootstyle="link")
        self.b5 = ttk.Button(self.skipButtons, text="<5- ", command=lambda : self.travel(-5), padding=0, bootstyle="link")
        self.b1 = ttk.Button(self.skipButtons, text="<1- ", command=lambda : self.travel(-1), padding=0, bootstyle="link")
        self.f1 = ttk.Button(self.skipButtons, text=" -1>", command=lambda : self.travel(1), padding=0, bootstyle="link")
        self.f5 = ttk.Button(self.skipButtons, text=" -5>", command=lambda : self.travel(5), padding=0, bootstyle="link")
        self.f10 = ttk.Button(self.skipButtons, text=" -10>", command=lambda : self.travel(10), padding=0, bootstyle="link")
    def up(self, *overflow):
        self.current = self.slider.get()
        self.audio.goto(self.current / self.seconds)
        self.updateSlider=True
    def down(self, *overflow):
        self.updateSlider=False
    def packChildren(self):
        self.b10.grid(column=0, row=0)
        self.b5.grid(column=1, row=0)
        self.b1.grid(column=2, row=0)
        self.f1.grid(column=3, row=0)
        self.f5.grid(column=4, row=0)
        self.f10.grid(column=5, row=0)
        self.skipButtons.grid(column=0, row=0, columnspan=7)
        self.label.grid(column=0, row=1, columnspan=2)
        self.slider.grid(column=2, row=1, columnspan=6, sticky="we")
    def travel(self, seconds):
        self.current+=seconds
        if self.current<0:
            self.current=0
        if self.current>self.seconds:
            self.current=self.seconds
        self.audio.goto(self.current / self.seconds)
        self.slider.configure(value=self.current)
    def update(self):
        new_text = "(%s / %s)"%(
            "%s:%02i"%(self.current//60, self.current%60),
            "%s:%02i"%(self.seconds//60, self.seconds%60)
        )
        if self.updateSlider:
            self.slider.config(value=self.current)
        self.label.configure(text = new_text)

top = ttk.Frame(root)
sc = songController(top)
sc.packChildren()
sc.grid(column=0, row=0, sticky="n")

seeker = seekerController(top, sc.audio)
seeker.packChildren()
seeker.grid(column=1, row=0, sticky="ew")

sc.audio.load("song.mp3")

top.pack(side = "top", anchor="w")

quit = ttk.Button(root, text="Quit", bootstyle = "danger", command=root.quit)
quit.pack(side = "bottom", anchor="e")

exit_main = False
def main_thread():
    a = 0
    while True:
        if exit_main:
            break
        seeker.current = int (sc.audio.player.get_time() / 1000)
        seeker.update()
        if a==7:
            seeker.seconds = int (sc.audio.player.get_length() / 1000)
            seeker.slider.config(to = seeker.seconds)
            a=-1
        sleep(0.2)
        a+=1

updateThread = Thread(target=main_thread, daemon=True)
updateThread.start()

root.mainloop()
exit_main = True