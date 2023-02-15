#v5 -- 
from time import sleep
from tkinter import *
from threading import Thread
from include.music_player_tools import *
from include.player import *
from include.songtable import *
from include.ui_elements import *
from components import source_manager

import os
import platform

themes = {
    "Bright Theme":{
        "background":rgb((210, 210, 255)),
        "text":rgb((0, 0, 0)),
        "default":rgb((200, 200, 200)),
        "selected":rgb((100, 100, 255)),
        "empty":rgb((200, 200, 255))
    },
    "Dark Theme":{
        "background":rgb((10, 10, 10)),
        "text":rgb((255, 255, 255)),
        "default":rgb((50, 50, 50)),
        "selected":rgb((50, 50, 255)),
        "empty":rgb((75, 75, 75))
    },
    "Special Theme":{
        "background":rgb((0,255,0)),
        "text":rgb((0, 0, 0)),
        "default":rgb((50, 100, 100)),
        "selected":rgb((50, 255, 50)),
        "empty":rgb((75, 75, 75))
    }
}
theme = themes["Bright Theme"]


quit = False

dir_sep = '/'
if platform.system() == "Windows":
    dir_sep = '\\'

playMan = audioPlayer()
playMan.loadPath("demo music/demo 1.mp3")


window = Tk()
window.title("Music Player")

top_panel = Frame(window)
song_label = Label(top_panel, text="demo 1")

mainmenu = Menu(window)

filemenu = Menu(mainmenu, tearoff = 0)
theme_menu = Menu(mainmenu, tearoff = 0)
mainmenu.add_cascade(label="App", menu=filemenu)
mainmenu.add_cascade(label="Theme", menu=theme_menu)

window.config(menu=mainmenu)

tables_panel = Frame(window)
menus = {
    "all songs": Frame(tables_panel),
    "library": Frame(tables_panel),
    "playlist": Frame(tables_panel)
}
table_menu = selection_array(tables_panel, ["all songs", "library", "playlist"])
tables = {
    "all songs":[song_table(menus["all songs"]), song_table(menus["all songs"])],
    "library":[song_table(menus["library"]), song_table(menus["library"])],
    "playlist":[song_table(menus["playlist"])]
}
playlist = tables["playlist"][0]
all_songs = tables["all songs"][0]

tables["library"][0].set_title("Library")
tables["library"][1].set_title("Playlist")
tables["library"][1].songs = playlist.songs
tables["all songs"][0].set_title("All")
tables["all songs"][1].set_title("Library")
tables["all songs"][1].songs = tables["library"][0].songs

directories = []
with open("saves/directories.txt", "r") as file:
    for i in file.readlines():
        directories+=[i.replace('\n', '')]
filter_directories = {}


def compileSongs(*args):
    all_songs.songs.clear()
    for i in directories:
        if not (i in filter_directories):
            filter_directories[i] = IntVar()
            filter_directories[i].set(1)
        if filter_directories[i].get() == 1:
            all_songs.songs += sorted(audioFile_scan(i, dir_sep))
    all_songs.update_buttons()
    update_directory_filter_menu()

filemenu.add_command(label = "Manage Sources", command=lambda : source_manager.manage_directories(window, directories, compileSongs, '/'))
filemenu.add_separator()
filemenu.add_command(label = "Manage Playlists")
filemenu.add_command(label = "Save Playlist")
filemenu.add_command(label = "Open Playlist")
filemenu.add_separator()
filemenu.add_command(label = "Quit", command=window.quit)


theme_selection = Menu(theme_menu)
theme_menu.add_command(label = "Manage Themes", command=compileSongs)
theme_menu.add_cascade(label = "Select Theme", menu=theme_selection)
theme_menu.add_separator()
theme_menu.add_checkbutton(label = "Enable Nothing New Mode")


selected_theme = StringVar()

bg_recolor = []
fg_recolor = []

def select_theme():
    global theme
    theme = themes[selected_theme.get()]
    table_menu["bg"] = theme["background"]
    table_menu.colors = theme
    table_menu.recolor()
    update_directory_filter_menu()

    for i in bg_recolor:
        i["bg"] = theme["background"]
    for i in fg_recolor:
        i["fg"] = theme["text"]
    for i in tables:
        menus[i]["bg"] = theme["background"]
        for n in tables[i]:
            n.colors = theme
            n.title_label["bg"] = theme["background"]
            n.title_label["fg"] = theme["text"]
            n["bg"] = theme["background"]
            n.innerFrame["bg"] = theme["background"]
            n.bBox["bg"] = theme["background"]
            n.update_buttons()
    # change all themes here
selected_theme.set("Bright Theme")
theme_selection.add_radiobutton(label="Dark Theme", variable=selected_theme, command=select_theme)
theme_selection.add_radiobutton(label="Bright Theme", variable=selected_theme, command=select_theme)
theme_selection.add_radiobutton(label="Special Theme", variable=selected_theme, command=select_theme)

def update_menu():
    for menu in menus:
        menus[menu].grid_forget()
    if table_menu.mode!=None:
        for table in tables[table_menu.mode]: 
            table.update_buttons()
        menus[table_menu.mode].grid(row=2)
table_menu.command=update_menu
table_menu.packItems()
table_menu.grid(row=1)
table_menu.set_mode("all songs")

for menu in menus:
    for i, table in enumerate(tables[menu]):
        # tables[menu] = song_table(menus[menu])
        table.make_buttons(15)
        table.pack_buttons()
        # table.title_label.pack_forget()
        table.grid(column=i, row=1)

# playlist
playMan.song_table=playlist

# library
def addto(source_table :song_table, destination_table :song_table):
    destination_table.songs += [source_table.song_path()]
    destination_table.update_buttons()
    source_table.next()
insert_to_playlist = Button(tables["library"][0].edit_buttons, text="copy to Playlist ->", pady=0, command=lambda:addto(tables["library"][0], tables["library"][1]))
insert_to_playlist.grid(column=3, row=0)
# all songs

insert_to_library = Button(tables["all songs"][0].edit_buttons, text="copy to Library ->", pady=0, command=lambda:addto(tables["all songs"][0], tables["all songs"][1]))
insert_to_library.grid(column=3, row=0)

dir_filter = Frame(menus["all songs"])
dir_filter_enabled = False
dir_filter_children = {}
def update_directory_filter_menu():
    global dir_filter_children
    for i in dir_filter_children:
        dir_filter_children[i].grid_forget()
    dir_filter_children.clear()
    for i, directory in enumerate(directories):
        if not (directory in filter_directories):
            filter_directories[directory] = IntVar()
            filter_directories[directory].set(1)
        dir_filter_children[directory] = Checkbutton(
            dir_filter, text=directory, variable=filter_directories[directory], command=compileSongs,
            foreground=theme["text"], background=theme["default"]
        )
        if filter_directories[directory].get():
            dir_filter_children[directory]["bg"] = theme["selected"]
        dir_filter_children[directory].grid(column=i%2, row=i//2)
update_directory_filter_menu()

def _toggle_dir_filter_():
    global dir_filter_enabled
    if dir_filter_enabled:
        toggle_dir_filter["bg"] = theme["default"]
        dir_filter_enabled=False
        dir_filter.grid_forget()
    else:
        toggle_dir_filter["bg"] = theme["selected"]
        dir_filter_enabled=True
        dir_filter.grid(column=0, columnspan=2, row=3)


toggle_dir_filter = Button(menus["all songs"], text="Filter", command=_toggle_dir_filter_, pady=0)
toggle_dir_filter.grid(column=0, row=2)


tables["all songs"][0].songs.clear()
compileSongs()
playlist.songs.clear()


volume = Scale(top_panel, from_=0, to=100, orient=HORIZONTAL, showvalue=False, sliderlength=15, length=250, border=1, command=playMan.set_volume)
volume.set(100)
playMan.set_volume(100)

seeker = Scale(top_panel, from_=0, to=100, orient=HORIZONTAL, showvalue=False, sliderlength=10, length=500, border=1, troughcolor=rgb((75,75,100)))

seeker_label = Label(top_panel, text="[0:00|0:00]")
volume_label = Label(top_panel, text="Volume: 100%")
seeker_override = False
def update_seeker():
    current_song = playlist.song_path()
    while True:
        seconds = playMan.player.get_time() / 1000
        length = playMan.player.get_length() / 1000

        song_name = playlist.get_name(current_song, '/')
        playlist.set_title("Playlist - %s"%song_name)
        song_label["text"] = song_name

        if seeker_override: seeker_label_text = "%s:%02i"%(int(length*(seeker.get()/100)/60), int(length*(seeker.get()/100))%60)
        else: seeker_label_text = "%s:%02i"%(int(seconds/60), int(seconds)%60)
        seeker_label["text"]="%s / %s"%(
                seeker_label_text,
                "%s:%02i"%(int(length/60), int(length)%60)
            )
        volume_label["text"]=f"Volume: {int(volume.get())}%"
        if current_song!=playlist.song_path():
            current_song=playlist.song_path()
            playMan.loadPath(current_song)
        if playMan.player.get_position()>0 and not seeker_override:
            seeker.set(100*playMan.player.get_position())
        if playMan.state=="playing" and not playMan.player.is_playing():
            sleep(0.1)
            if not playMan.player.is_playing():
                playMan.next()
        if quit: break
def seeker_press(dat):
    global seeker_override
    seeker_override=True
def seeker_release(dat):
    global seeker_override, play_state
    seeker_override=False
    playMan.player.set_position(seeker.get()/100)

playCtrl = play_panel(top_panel, playMan)
playCtrl.packItems(playMan.state)


seeker.bind("<Button-1>", seeker_press)
seeker.bind("<ButtonRelease-1>", seeker_release)

song_label.grid(column=0, row=0, columnspan=3, padx=1, sticky=W)
playCtrl.grid(column=0, row=1, rowspan=2, padx=1, pady=0, sticky=W)
volume_label.grid(column=1, row=1, rowspan=1, padx=0, pady=0)
seeker_label.grid(column=1, row=2, rowspan=1, padx=0, pady=0)
volume.grid(column=2, row=1, rowspan=1, padx=0, pady=0, sticky=W)
seeker.grid(column=2, row=2, rowspan=1, padx=0, pady=0, sticky=W)

seekbar_thread = Thread(target=update_seeker, daemon=True)
seekbar_thread.start()

top_panel.pack(side=TOP, anchor=W)
tables_panel.pack()

fg_recolor = [song_label,insert_to_playlist, insert_to_library, toggle_dir_filter,
    song_label, volume_label, seeker_label,]
bg_recolor = fg_recolor + [playCtrl, top_panel, window, tables_panel, dir_filter]
frames = []
select_theme()


window.mainloop()
quit=True
playMan.exit()