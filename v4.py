#v4 -- 
from tkinter import *
from player import *

playMan = player()
playMan.loadPath("demo music/demo 1.mp3")

class playPanel(Frame):
    def __init__(self, master, playManager):
        Frame.__init__(self, master)
        self.images = {
            "playing":PhotoImage(file = "images/playButton.png"),
            "paused":PhotoImage(file = "images/pauseButton.png"),
            "stopped":PhotoImage(file = "images/stopButton.png"),
            "previous":PhotoImage(file = "images/previousButton.png"),
            "next":PhotoImage(file = "images/nextButton.png"),
            "empty":PhotoImage(file = "images/emptyButton.png"),
        }
        for n in self.images:
            self.images[n] = self.images[n].zoom(3)
        for n in self.images:
            self.images[n] = self.images[n].subsample(2)
        self.playButton = Button(self, image=self.images["playing"], command=lambda:self.playToggle(playManager))
        self.stopButton = Button(self, image=self.images["stopped"], command=lambda:self.stop(playManager))
        self.previousButton = Button(self, image=self.images["previous"])
        self.nextButton = Button(self, image=self.images["next"])
    def forgetItems(self):
        self.playButton.grid_forget()
        self.stopButton.grid_forget()
        self.previousButton.grid_forget()
        self.nextButton.grid_forget()
    def packItems(self, playState):
        # self.forgetItems()
        if playState=="playing":
            self.playButton["image"]=self.images["paused"]
            self.stopButton["image"]=self.images["stopped"]
            self.playButton.grid(column=0, row=0)
            self.stopButton.grid(column=1, row=0)
            self.previousButton.grid(column=0, row=1)
            self.nextButton.grid(column=1, row=1)
        elif playState=="paused":
            self.playButton["image"]=self.images["playing"]
            self.stopButton["image"]=self.images["stopped"]
            self.playButton.grid(column=0, row=0)
            self.stopButton.grid(column=1, row=0)
            self.previousButton.grid(column=0, row=1)
            self.nextButton.grid(column=1, row=1)
        elif playState=="stopped":
            self.playButton["image"]=self.images["playing"]
            self.stopButton["image"]=self.images["empty"]
            self.playButton.grid(column=0, row=0)
            self.stopButton.grid(column=1, row=0)
            self.previousButton.grid(column=0, row=1)
            self.nextButton.grid(column=1, row=1)
    def playToggle(self, playManager):
            playManager.playToggle()
            self.packItems(playManager.state)
    def stop(self, playManager):
            playManager.stop()
            self.packItems("stopped")
    
            
            


window = Tk()
window.title("VWES - VLC with Extra Steps")

playCtrl = playPanel(window, playMan)
playCtrl.packItems(playMan.state)
playCtrl.pack(side=TOP, anchor=W)

window.mainloop()