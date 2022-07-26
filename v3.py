#v3 -- still ugly, v2 re-attempt (not really a rewrite, but sort of)
#(v3 -- actually the final version i just have to rewrite it a lot more)
from tkinter import *
import vlc
import os

#my extras
from music_player_tools import *
from songtable import *

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

playlist = []
selected = 0
playing = "stopped"
seek_override = False


def play_toggle():
    global playing
    if playing=="stopped":
        playing="playing"
    elif playing=="paused":
        playing="playing"
    elif playing=="playing":
        playing="paused"
    update_playButton()

def update_playButton():
    global playing
    if playing == "stopped":
        play_button["text"]="Play"
    elif playing == "playing":
        play_button["text"]="Pause"
    elif playing == "paused":
        play_button["text"]="Resume"

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

songs_table = songTable(song_panel)
songs_table.title_label.pack_forget()
songs_table.make_buttons(20)
songs_table.pack_buttons()
songs_table.import_songs(temp_songs)


# play & stop & next & previous
player_panel = Frame(left_panel, highlightbackground=rgb((0, 0, 0)), highlightthickness=1)

play_button = Button(player_panel)

play_button = Button(player_panel, text="Play", command=play_toggle, padx=1)
stop_button = Button(player_panel, text="Stop", padx=1)
next_button = Button(player_panel, text="Next >", pady=0)
previous_button = Button(player_panel, text="< Prev", pady=0)

# right side frame
right_panel = Frame(window, highlightbackground=rgb((0, 0, 0)), highlightthickness=1)

# playlist manager
playlist_panel = Frame(right_panel, highlightbackground=rgb((0, 0, 100)), highlightthickness=2)
playlist_label = Label(playlist_panel, text="Playlist Manager")

playlist_table = songTable(playlist_panel)
playlist_table.set_title("Playlist")
playlist_table.make_buttons(20)
playlist_table.pack_buttons()

# seek & volume
slider_panel = Frame()

### packing

# left panel
left_panel.pack(side=LEFT, anchor=NW, fill=BOTH, expand=True)

# play & stop & next & previous buttons
play_button.grid(column=0, row=0)
stop_button.grid(column=1, row=0)
next_button.grid(column=1, row=1)
previous_button.grid(column=0, row=1)

player_panel.pack(side=TOP, anchor=NW)

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