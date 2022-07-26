import os

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

# def get_name(directory, seperator):
#     parts = directory.rsplit(seperator, 1)
#     fileName = parts[1]
#     return fileName.rsplit(".mp3", 1)[0]

# def generate_names(song_list):
#     new_names=[]
#     for n in song_list:
#         new_names.append(get_name(n, "/"))
#     return new_names

def audioFile_scan(directory, seperator):
    
    found_songs=[]

    for n in os.listdir(directory):
        if os.path.isdir(directory+seperator+n):
            audioFile_scan(directory+seperator+n, seperator)
        elif ".mp3" in n and not directory+seperator+n in found_songs:
            found_songs.append(directory+seperator+n)
    
    return found_songs
