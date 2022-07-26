#v1 -- just a test
import tkinter as tk
import vlc


p = vlc.MediaPlayer("demo music/demo 1.mp3")
vlc.MediaPlayer("demo music/demo 2.mp3")

songs = ["demo music/demo 1.mp3", "demo music/demo 2.mp3"]
song_selected=0

scr = tk.Tk()

scr.title("Super Music Player")

playing = "paused"

def update_button():
    pass

def play_toggle():
    global playing

    if playing=="paused":
        playing = "playing"
        a["text"]="pause"
        p.play()
    elif playing=="playing":
        playing = "paused"
        a["text"]="resume"
        p.pause()

def play_next():
    global songs, song_selected
    song_selected+=1
    if song_selected>len(songs)-1:
        song_selected=0
    p.stop()
    song_label["text"]=songs[song_selected]
    p.set_media(vlc.Media(songs[song_selected]))
    p.play()


song_label = tk.Label(scr, text=songs[song_selected])
song_label.grid(column=0, row=0)

a = tk.Button(scr, text="resume", command=play_toggle)
a.grid(column=0, row=1)
b = tk.Button(scr, text="prev")
b.grid(column=0, row=2)
c = tk.Button(scr, text="next", command=play_next)
c.grid(column=1, row=2)




scr.mainloop()
