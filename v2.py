#v2 -- 
import tkinter as tk
import vlc
import os
import include.music_player_tools as music_player_tools, include.player as player, include.ui_elements as ui_elements
def rgb_hack(rgb):
    return "#%02x%02x%02x" % rgb

player = vlc.MediaPlayer()
play_state="stopped"

# duration = player.get_length()


window = tk.Tk()
window.title("VWES - VLC with Extra Steps")

seeker_override=False

song_queue = music_player_tools.audioFile_scan("/home/kken/Music", "/") + music_player_tools.audioFile_scan("/media/kken/9C33-6BBD/Music", "/")
selected_song = 0

# for n in os.listdir("/home/pro/Music"):
#     if ".mp3" in n:
#         song_queue.append("/home/pro/Music/"+n)

def find_songs(folder_path):
    for n in os.listdir(folder_path):
        if ".mp3" in n:
            song_queue.append(folder_path+"/"+n)
        elif os.path.isdir(folder_path+"/"+n):
            find_songs(folder_path+"/"+n)

find_songs("/home/pro/Music")

def song_loop():
    global duration, seeker_edit, play_state
    window.after(250, song_loop)
    if player.get_position()>0 and not seeker_override:
        seek.set(100*player.get_position())
    if play_state=="playing" and not player.is_playing():
        next_song()
    if len(song_box.curselection())==0:
        song_box.select_set(selected_song, selected_song)

def load_song(song_path):
    global duration, play_state
    player.stop()
    player.set_media(vlc.Media(song_path))
    seek.set(0)
    if play_state=="playing":
        player.play()
    else:
        play_state="stopped"
    update_ui_playbutton()
    duration=player.get_length()
def seeker_press(dat):
    global seeker_override
    seeker_override=True
def seeker_release(dat):
    global seeker_override, play_state
    seeker_override=False
    player.set_position(seek.get()/100)

def set_volume(volume):
    player.audio_set_volume(int(volume))


def play_toggle():
    global play_state
    if play_state=="playing":
        play_state="paused"
        player.pause()
    elif play_state=="paused" or play_state=="stopped":
        play_state="playing"
        player.play()
    update_ui_playbutton()
def stop_song():
    global play_state
    player.stop()
    seek.set(0)
    play_state="stopped"
    update_ui_playbutton()
def update_ui_playbutton():
    global play_state
    if play_state=="playing":
        play_button["text"]="Pause"
    if play_state=="paused":
        play_button["text"]="Resume"
    if play_state=="stopped":
        play_button["text"]="Play"

def get_song_from_queue():
    load_song(song_box.get(tk.ACTIVE))

def next_song():
    global selected_song
    song=selected_song+1
    if song>len(song_queue)-1:
        song=0
    selected_song=song
    song_box.select_clear(0, len(song_queue)-1)
    song_box.select_set(song, song)
    song_box.activate(song)
    get_song_from_queue()
def previous_song():
    global selected_song
    if(len(song_box.curselection())>0):
        song=song_box.curselection()[len(song_box.curselection())-1]-1
    else:
        song=selected_song
    if song<0:
        song=len(song_queue)-1
    selected_song=song
    song_box.select_clear(0, len(song_queue)-1)
    song_box.select_set(song, song)
    song_box.activate(song)
    get_song_from_queue()
play_image = tk.PhotoImage(file="images/playButton.png")
top_frame = tk.Frame(window)
play_button=tk.Button(top_frame, text="Play", command=play_toggle, image=play_image)
next_button=tk.Button(top_frame, text="Next >", command=next_song)
previous_button=tk.Button(top_frame, text="< Prev", command=previous_song)
stop_button=tk.Button(top_frame, text="Stop", command=stop_song)

# load_song("demo music/demo 2.mp3")

center_frame = tk.Frame(window)

volume = tk.Scale(center_frame, from_=0, to=500, orient=tk.HORIZONTAL, sliderlength=15, length=250, border=1, command=set_volume)
volume.set(100)
set_volume(100)


seek = tk.Scale(center_frame, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=0, sliderlength=10, length=500, border=5, troughcolor=rgb_hack((75,75,100)))
seek.bind("<Button-1>", seeker_press)
seek.bind("<ButtonRelease-1>", seeker_release)

# songs stuff

queue_frame = tk.Frame(window)
edit_buttons = tk.Frame(queue_frame)

song_box = tk.Listbox(queue_frame, selectmode=tk.SINGLE)

for song in song_queue:
    song_box.insert(tk.END, song)

up_button=tk.Button(edit_buttons, text="↑", padx=0, pady=0)
down_button=tk.Button(edit_buttons, text="↓", padx=0, pady=0)
remove_button=tk.Button(edit_buttons, text="x", padx=0, pady=0)
select_button=tk.Button(edit_buttons, text="select", padx=0, pady=0, command=get_song_from_queue)

scrollbar = tk.Scrollbar(
    queue_frame,
    orient=tk.VERTICAL,
    command=song_box.yview,
)

song_box.config(yscrollcommand=scrollbar.set)

up_button.grid(column=0, row=0)
down_button.grid(column=1, row=0)
remove_button.grid(column=2, row=0)
select_button.grid(column=3, row=0)

edit_buttons.pack(side=tk.BOTTOM, anchor=tk.W)

scrollbar.pack(side=tk.RIGHT, anchor=tk.W, expand=tk.YES, fill=tk.Y)
song_box.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES, fill=tk.BOTH)


# packing
top_frame.pack(side=tk.TOP, anchor=tk.NW)
play_button.grid(column=0, row=0)
stop_button.grid(column=1, row=0)
next_button.grid(column=1, row=1)
previous_button.grid(column=0, row=1)

center_frame.pack(side=tk.BOTTOM, anchor=tk.CENTER)
seek.pack(side=tk.BOTTOM, anchor=tk.SE)
volume.pack(side=tk.RIGHT, anchor=tk.SE)

queue_frame.pack(side=tk.LEFT, anchor=tk.W, expand=tk.YES, fill=tk.BOTH)

window.after(2000, song_loop)
window.mainloop()
