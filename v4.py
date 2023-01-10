#v4 -- 
from tkinter import *
from include.player import *
from include.ui_elements import *

playMan = audioPlayer()
playMan.loadPath("demo music/demo 1.mp3")


window = Tk()
window.title("Music Player")

playCtrl = play_panel(window, playMan)
playCtrl.packItems(playMan.state)
playCtrl.pack(side=TOP, anchor=W)

window.mainloop()