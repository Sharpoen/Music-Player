#v5 -- 
from time import sleep
from tkinter import *
from threading import Thread
from include.music_player_tools import *
from include.player import *
from include.songtable import *
from include.ui_elements import *
import os

quit = False

dir_sep = '/'

playMan = audioPlayer()
playMan.loadPath("demo music/demo 1.mp3")


window = Tk()
window.title("Music Player")

top_panel = Frame(window)
song_label = Label(top_panel, text="demo 1")

mainmenu = Menu(window)

filemenu = Menu(mainmenu, tearoff = 0)
mainmenu.add_cascade(label="File", menu=filemenu)

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

def compileSongs(*args):
    all_songs.songs.clear()
    for i in directories:
        all_songs.songs += audioFile_scan(i, dir_sep)
    all_songs.update_buttons()
def manage_directories():
    dir_window = Toplevel(window)
    dir_window.title("Directory Manager")
    dir_lookup_entry_label = Label(dir_window, text="Directory")
    dir_lookup_entry = Entry(dir_window, width=50)
    all_directories = song_table(dir_window)
    all_directories.set_title("All Directories")
    all_directories.songs = directories
    all_directories.song_names = all_directories.songs
    def return_same(a, *burn):
        return a
    something = {"cur_dir":'/'}
    possibilities = selection_array(dir_window, [])
    def select_possibility():
        dir_name = possibilities.mode
        if not type(dir_name) == str: return
        new_dir = ''+something["cur_dir"]
        while dir_sep+dir_sep in new_dir:
            new_dir = new_dir.replace(dir_sep+dir_sep, dir_sep)
        if dir_name == "..":
            new_dir = new_dir.rsplit(dir_sep, 2)[0]
            dir_lookup_entry.delete(0, END)
            dir_lookup_entry.insert(0, new_dir+'/')
            update_possibilities()
            return
        if os.path.isdir(new_dir + dir_name + '/'): new_dir+=dir_name + '/'

        dir_lookup_entry.delete(0, END)
        dir_lookup_entry.insert(0, new_dir)
        update_possibilities()
    possibilities.command = select_possibility
    possibilities.stack = 20

    def update_possibilities(*burn):
        cur_dir = dir_lookup_entry.get()
        if os.path.isdir(cur_dir+dir_sep):
            cur_dir+=dir_sep
        if burn and os.path.isdir(cur_dir+burn[0].char+dir_sep):
            cur_dir+=burn[0].char+dir_sep
        if os.path.isdir(cur_dir):
            possibilities.options.clear()
            something["cur_dir"] = cur_dir
            new_options = [".."] + os.listdir(cur_dir)
            for option in new_options:
                if option[0]=='.' and option!= "..": continue
                possibilities.options += [option]
            possibilities.generate_buttons()
            possibilities.packItems()
    update_possibilities()

    def save_directories():
        with open("saves/directories.txt", "w") as file:
            for n in all_songs.songs:
                file.write("%s\n"%n)
    save_button = Button(all_directories.edit_buttons, pady=0, command = save_directories, text = "Save")
    save_button.grid(column=3, row=0)

    dir_lookup_entry.bind('<Key>', update_possibilities)

    all_directories.generate_names = return_same
    all_directories.label_length = 50

    all_directories.make_buttons(5)
    all_directories.update_buttons()
    all_directories.pack_buttons()

    def insert_directory():
        new_dir = dir_lookup_entry.get()
        if os.path.isdir(new_dir) and not new_dir in all_songs.songs:
            all_directories.songs+=[new_dir]
            all_directories.update_buttons()
            all_songs.songs.clear()
            all_songs.update_buttons()
            compileSongs()

    def new_delete():
        all_directories.remove_song(all_directories.selected_song)
        compileSongs()
    all_directories.remove_button["command"] = new_delete

    insert_directory_button = Button(dir_window, text="+", command=insert_directory, padx=0, pady=0)
    
    dir_lookup_entry_label.grid(column=0, row=0)
    dir_lookup_entry.grid(column=1, row=0, sticky=W+E)
    insert_directory_button.grid(column=2, row=0, sticky=W)
    possibilities.grid(column=0, row=1, columnspan=4)
    all_directories.grid(column=0, row=3, columnspan=2)

filemenu.add_command(label = "Manage Directories", command=manage_directories)

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

for menu in menus:
    for i, table in enumerate(tables[menu]):
        # tables[menu] = song_table(menus[menu])
        table.make_buttons(10)
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

tables["all songs"][0].songs.clear()
compileSongs()
playlist.songs += sorted(audioFile_scan("/media/kken/9C33-6BBD/Music/Kansas", '/')) + sorted(audioFile_scan("/media/kken/9C33-6BBD/Music/Kate Bush", '/'))


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
        playlist.set_title(song_name)
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
window.mainloop()
quit=True
playMan.exit()