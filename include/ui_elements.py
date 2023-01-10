from tkinter import *
from include.music_player_tools import *

class play_panel(Frame):
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
        self.nextButton = Button(self, image=self.images["next"], command=playManager.next)
        self.previousButton = Button(self, image=self.images["previous"], command=playManager.previous)
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

class selection_array(Frame):
    def __init__(self, master, options):
        Frame.__init__(self, master)
        self.colors = {
            "default":rgb((200, 200, 200)),
            "selected":rgb((100, 100, 255))
        }
        self.options = options
        self.mode = None
        self.stack = 1
        self.buttons = []
        self.generate_buttons()
        self.command = self.skip
        self.args = []
    def skip(self):pass
    def generate_buttons(self):
        self.forgetItems()
        self.buttons.clear()
        for option in self.options:
            self.buttons.append(
                Button(
                    self, text=option, command=lambda option=option:self.set_mode(option), background=self.colors["default"], pady=0
                    )
                )
    def packItems(self):
        for i, button in enumerate(self.buttons):
            button.grid(column=i//self.stack, row=i%self.stack, sticky = "EW")
    def forgetItems(self):
        for button in self.buttons:
            button.grid_forget()
    def set_mode(self, mode):
        for button, option in zip(self.buttons, self.options):
            if mode==option:button["bg"]=self.colors["selected"]
            else:button["bg"]=self.colors["default"]
        self.mode=mode
        self.command(*self.args)