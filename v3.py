#v3 -- 
from tkinter import *
import vlc
import os

#my extras
from include.music_player_tools import *
from include.songtable import *
from include.ui_elements import *
from include.player import *

window = Tk()
player = vlc.MediaPlayer()

os.listdir("/home/pro/")

def get_name(directory, seperator):
    parts = directory.rsplit(seperator, 1)
    fileName = parts[1]
    return fileName.rsplit(".mp3", 1)[0]

def generate_names(song_list):
    new_names=[]
    for n in song_list:
        new_names.append(get_name(n, "/"))
    return new_names


# audioFile_scan("/home/pro/Music", "/")


# with open("song paths.txt", mode="a") as song_paths_file:
#     for n in song_list:
#         song_paths_file.write("\n"+n)

temp_songs=[]

with open("song paths.txt", mode="r") as song_paths:
    a=song_paths.readlines()
    for b in a:
        n=b.rsplit("\n", 1)[0]
        # if os.path.isfile(n):
        # print(n)
        if os.path.isfile(n) and not n in temp_songs:
            temp_songs.append(n)

# print(song_list)

print(audioFile_scan("/home/kken/Music", "/"))

playlist = audioFile_scan("/home/kken/Music", "/")
selected = 0
playing = "stopped"
seek_override = False






def qsec_loop(): #quarter second loop
    window.after(250, qsec_loop)

# left side frame
left_panel = Frame(window)

# song importer

# insert manager
song_panel = Frame(left_panel, highlightbackground=rgb((0, 0, 50)), highlightthickness=2)
song_label = Label(song_panel, text="Song Manager")

def creater_popup():
    global song_list, song_names
    creater_window = Toplevel(window)
    creater_window.title("Create & Edit Insert Methods")
    close_creater_window = Button(creater_window, text="Close", command=creater_window.destroy, pady=0)
    close_creater_window.pack(side=BOTTOM, anchor=SE)

open_creater_button = Button(song_panel, text="Manage Methods", command=creater_popup)

def insert_song():
    if songs_table.selected_song>=0 and songs_table.selected_song<len(songs_table.songs):
        playlist_table.import_songs([songs_table.songs[songs_table.selected_song]])
        songs_table.select_song(songs_table.selected_song+1)


insert_button = Button(song_panel, text="Add Selected Song", pady=0, command=insert_song)

songs_table = song_table(song_panel)
songs_table.title_label.pack_forget()
songs_table.make_buttons(20)
songs_table.pack_buttons()
songs_table.import_songs(temp_songs)


# play & stop & next & previous
song_player = audioPlayer()
player_panel = play_panel(window, song_player)

# right side frame
right_panel = Frame(window, highlightbackground=rgb((0, 0, 0)), highlightthickness=1)

# playlist manager
playlist_panel = Frame(right_panel, highlightbackground=rgb((0, 0, 100)), highlightthickness=2)
playlist_label = Label(playlist_panel, text="Playlist Manager")

playlist_table = song_table(playlist_panel)
playlist_table.set_title("Playlist")
playlist_table.make_buttons(20)
playlist_table.pack_buttons()

# seek & volume
slider_panel = Frame()

### packing

# play & stop & next & previous buttons
song_player.loadPath("demo music/demo 1.mp3")
player_panel.packItems(playing)
player_panel.pack(side=TOP, anchor=NW)

# left panel
left_panel.pack(side=LEFT, anchor=NW, fill=BOTH, expand=True)


# song manager


song_label.pack(side=TOP, anchor=CENTER)
open_creater_button.pack(side=TOP, anchor=W)
insert_button.pack(side=TOP, anchor=W)

songs_table.pack(side=TOP, anchor=CENTER, expand=True, fill=BOTH)

song_panel.pack(side=TOP, anchor=CENTER, fill=BOTH, expand=True)



#right side panel
right_panel.pack(side=RIGHT, anchor=E, fill=BOTH, expand=True)

# playlist manager

playlist_label.pack(side=TOP, anchor=CENTER)

playlist_panel.pack(side=LEFT, anchor=SE, fill=BOTH, expand=True)

playlist_table.pack(side=TOP, anchor=CENTER, expand=True, fill=BOTH)


window.title("VWES - VLC with Extra Steps")
window.after(2000, qsec_loop)
window.mainloop()