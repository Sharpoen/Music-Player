from tkinter import *
from include.music_player_tools import *


class song_table(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        
        self.colors = {
            "text":rgb((0, 0, 0)),
            "default":rgb((200, 200, 200)),
            "selected":rgb((100, 100, 255)),
            "empty":rgb((200, 200, 255))
        }
        
        self.font="TkFixedFont"

        self.dir_seperator="/"

        self.title_label = Label(self, text="Song Table")
        self.title_label.pack(side=TOP, anchor=CENTER)

        self.bonds = [] 
        self.songs = []
        self.song_names = []
        self.selected_song=0
        self.y_offset=0

        self.innerFrame = Frame(self)
        self.innerFrame.pack(side = TOP, anchor=W, expand=True, fill=BOTH)

        self.bBox = Frame(self.innerFrame, highlightbackground=rgb((0, 0, 0)), highlightthickness=1)
        self.bBox.pack(side = LEFT, anchor=W, expand=True, fill=BOTH)
        # self.bBox.pack(side = LEFT, anchor=W)

        self.label_length = 50
        self.label_scroll = 0

        self.sButtons = []

        self.scrollbar = Scale(self.innerFrame, from_=-1, to=10, orient=VERTICAL, showvalue=0, sliderlength=15, command=self.set_y_offset)
        self.scrollbar.pack(side=LEFT, anchor=W, expand=True, fill=Y)
        self.scrollbar.bind("<Button-4>", self.scroll)
        self.scrollbar.bind("<Button-5>", self.scroll)
        # self.scrollbar.bind("<MouseWheel>", self.scroll)

        self.edit_buttons = Frame(self)
        self.swap_up_button=Button(self.edit_buttons, text="↑", pady=0, command=self.swap_up)
        self.swap_down_button=Button(self.edit_buttons, text="↓", pady=0, command=self.swap_down)
        self.remove_button=Button(self.edit_buttons, text="x", pady=0, command=lambda: self.remove_song(self.selected_song))

        self.swap_up_button.grid(column=0, row=0)
        self.swap_down_button.grid(column=1, row=0)
        self.remove_button.grid(column=2, row=0)
        
        self.edit_buttons.pack(side=BOTTOM, anchor=NW)

    def bond(self, connection):
        self.bonds += [connection]
        connection.bonds += [self]

    def get_label(self, text):
        if len(text)>self.label_length:
            return text[0:self.label_length-1]
        else:
            return text + " " * (self.label_length-len(text))
        
    def update_scrollbar(self):
        self.scrollbar["to"]=len(self.songs)-(len(self.sButtons)-1)

    def scroll(self, value, *burn):
        if value.num==4:
            self.set_y_offset(self.y_offset-1)
        if value.num==5:
            self.set_y_offset(self.y_offset+1)
        self.scrollbar.set(self.y_offset)

    def set_y_offset(self, offset):
        if int(offset)!=self.y_offset:
            self.y_offset=int(offset)
            self.update_buttons()

    def swap_up(self):
        if self.swap_song(self.selected_song-1, self.selected_song):
            self.selected_song-=1
        self.update_buttons()
    def swap_down(self):
        if self.swap_song(self.selected_song+1, self.selected_song):
            self.selected_song+=1
        self.update_buttons()

    def set_title(self, title):
        self.title_label["text"]=title
    def do_nothing(*filler_parameters):
        pass
    def get_name(self, directory :str, seperator :str):
        if type(directory)!=str:
            return "error"
        if type(seperator)!=str:
            return "error"
        if self.songs:
            parts = directory.rsplit(seperator, 1)
            fileName=""
            if len(parts)>1:
                fileName = parts[1]
            else:
                fileName = parts[0]

            return fileName.rsplit(".mp3", 1)[0]

    def generate_names(self, song_list, seperator):
        new_names=[]
        for n in song_list:
            new_names.append(self.get_name(n, seperator))
        return new_names
    def select_song(self, song_number):
        self.selected_song=song_number
        self.update_buttons()
    def song_path(self): 
        if self.selected_song>=0 and self.selected_song<len(self.songs):
            return self.songs[self.selected_song]
    def next(self):
        self.selected_song+=1
        if self.selected_song>=len(self.songs):self.selected_song=0
        self.update_buttons()
        if len(self.songs) == 0: return None
        return self.songs[self.selected_song]
    def previous(self):
        self.selected_song-=1
        if self.selected_song<0:self.selected_song=len(self.songs)-1
        self.update_buttons()
        return self.songs[self.selected_song]
    def swap_song(self, a, b):
        if a>=0 and b>=0 and a<len(self.songs) and b<len(self.songs):
            self.songs[a], self.songs[b] = self.songs[b], self.songs[a]
            self.update_buttons()
            return True
        else:
            self.update_buttons()
            return False

    def make_buttons(self, ama :int):
        for i in range(len(self.sButtons)):
            self.sButtons[i].destroy()
        
        newButtons = []

        for i in range(ama):
            if i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                newButtons.append(Button(self.bBox, font=self.font, anchor=W, text="  %s  "%self.get_label(self.song_names[i+self.y_offset]), pady=0, command=lambda i=i:self.select_song(i+self.y_offset), fg=self.colors["text"]))
            else:
                newButtons.append(Button(self.bBox, font=self.font, anchor=W, text="  "+"-"*self.label_length+"  ", pady=0, command=self.do_nothing, bg=self.colors["empty"], fg=self.colors["text"]))
            
            if i+self.y_offset==self.selected_song:
                if i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                    newButtons[i]["text"]="[ %s ]"%self.get_label(self.song_names[i+self.y_offset])
                newButtons[i]["bg"]=self.colors["selected"]
            elif i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                newButtons[i]["bg"]=self.colors["default"]

            newButtons[i].bind("<Button-4>", self.scroll)
            newButtons[i].bind("<Button-5>", self.scroll)
       
        self.sButtons=newButtons.copy()

    def update_buttons(self, *args):
        if len(args)>=1: return
        if self.scrollbar["to"]!=len(self.songs):
            self.update_scrollbar()
        self.song_names = self.generate_names(self.songs, self.dir_seperator)

        for i in range(len(self.sButtons)):
            self.sButtons[i]["fg"] = self.colors["text"]
            if i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                self.sButtons[i]["text"] = "  %s  "%self.get_label(self.song_names[i+self.y_offset])
                self.sButtons[i]["command"] = lambda i=i:self.select_song(i+self.y_offset)
            else:
                self.sButtons[i]["text"] = "  "+"-"*self.label_length+"  "
                self.sButtons[i]["command"] = self.do_nothing
                self.sButtons[i]["bg"]=self.colors["empty"]
            
            if i+self.y_offset==self.selected_song:
                if i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                    self.sButtons[i]["text"]="[ %s ]"%self.get_label(self.song_names[i+self.y_offset])
                self.sButtons[i]["bg"]=self.colors["selected"]
            elif i+self.y_offset>=0 and i+self.y_offset<len(self.songs):
                self.sButtons[i]["bg"]=self.colors["default"]
        for bond in self.bonds:
            bond.update_buttons(False)

    def pack_buttons(self):
        for i in range(len(self.sButtons)):
            self.sButtons[i].grid(column=0, row=i*2)

    def import_songs(self, songs):
        for song in songs:
            self.songs.append(song)

        self.song_names=self.generate_names(self.songs, self.dir_seperator)

        self.update_buttons()
    
    def remove_song(self, song_number):
        if song_number>=0 and song_number < len(self.songs):
            self.songs.pop(song_number)
        if self.selected_song>len(self.songs)-1:
            self.selected_song=len(self.songs)-1
        self.update_buttons()

def demo():
    window = Tk()

    mainframe = Frame(window)

    new_box = song_table(mainframe)
    new_box.make_buttons(10)
    new_box.pack_buttons()
    new_box.pack(expand=True, fill=BOTH)

    new_box.make_buttons(25)
    new_box.pack_buttons()

    new_box.import_songs(["song 1", "song 2", "song 3", "song 4", "song 5", "song 6", "song 7", "song 8"])
    new_box.remove_song(2)

    mainframe.pack()

    window.title("Song Box Demo")
    window.mainloop()


if __name__ == "__main__":
    demo()
