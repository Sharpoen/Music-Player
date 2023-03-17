from tkinter import *
from include.ui_elements import *
from include.songtable import *



_manage_directories_open_ = False
def manage_directories(master : Tk, directories : list, compile_songs : "function", directory_seperator : str):
    global _manage_directories_open_
    if _manage_directories_open_ == True:
        return
    _manage_directories_open_ = True
    window = Toplevel(master)
    def close():
        global _manage_directories_open_
        _manage_directories_open_ = False
        window.destroy()

    window.protocol("WM_DELETE_WINDOW", close)
    window.title("Source Manager")

    
    dir_lookup_entry_label = Label(window, text="Directory")
    dir_lookup_entry = Entry(window, width=50)
    all_directories = song_table(window, directory_seperator)
    all_directories.set_title("All Directories")
    all_directories.songs = directories
    all_directories.song_names = all_directories.songs
    def return_same(a, *burn):
        return a
    something = {"cur_dir":directory_seperator}
    possibilities = selection_array(window, [])
    def select_possibility():
        dir_name = possibilities.mode
        if not type(dir_name) == str: return
        new_dir = ''+something["cur_dir"]
        while directory_seperator+directory_seperator in new_dir:
            new_dir = new_dir.replace(directory_seperator+directory_seperator, directory_seperator)
        if dir_name == "..":
            new_dir = new_dir.rsplit(directory_seperator, 2)[0]
            dir_lookup_entry.delete(0, END)
            dir_lookup_entry.insert(0, new_dir+directory_seperator)
            update_possibilities()
            return
        if os.path.isdir(new_dir + dir_name + directory_seperator): new_dir+=dir_name + directory_seperator

        dir_lookup_entry.delete(0, END)
        dir_lookup_entry.insert(0, new_dir)
        update_possibilities()
    possibilities.command = select_possibility
    possibilities.stack = 5

    def update_possibilities(*burn):
        cur_dir = dir_lookup_entry.get()
        if os.path.isdir(cur_dir+directory_seperator):
            cur_dir+=directory_seperator
        if burn and os.path.isdir(cur_dir+burn[0].char+directory_seperator):
            cur_dir+=burn[0].char+directory_seperator
        if os.path.isdir(cur_dir):
            possibilities.options.clear()
            something["cur_dir"] = cur_dir
            new_options = [".."]
            for name in os.listdir(cur_dir):
                if os.path.isdir("%s/%s"%(cur_dir, name)):
                    new_options += [name]
            for option in new_options:
                if option[0]=='.' and option!= "..": continue
                possibilities.options += [option]
            possibilities.stack = 1 + int(len(possibilities.options)/7)
            possibilities.generate_buttons()
            possibilities.packItems()
    update_possibilities()

    def save_directories():
        with open("saves/directories.txt", "w") as file:
            for n in all_directories.songs:
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
        if os.path.isdir(new_dir) and not new_dir in all_directories.songs:
            all_directories.songs+=[new_dir]
            all_directories.update_buttons()
            compile_songs()

    def new_delete():
        all_directories.remove_song(all_directories.selected_song)
        compile_songs()
    all_directories.remove_button["command"] = new_delete

    insert_directory_button = Button(window, text="+", command=insert_directory, padx=0, pady=0)
    
    dir_lookup_entry_label.grid(column=0, row=0)
    dir_lookup_entry.grid(column=1, row=0, sticky=W+E)
    insert_directory_button.grid(column=2, row=0, sticky=W)
    possibilities.grid(column=0, row=1, columnspan=3)
    all_directories.grid(column=0, row=3, columnspan=2)