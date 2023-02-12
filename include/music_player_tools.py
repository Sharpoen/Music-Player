import os

def rgb(rgb):
    return "#%02x%02x%02x" % rgb

def audioFile_scan(directory, seperator):
    
    found_songs=[]

    if not os.path.isdir(directory):
        print("%s: not a directory"%directory)
        return []
    
    for n in os.listdir(directory):
        if os.path.isdir(directory+seperator+n):
            found_songs+=audioFile_scan(directory+seperator+n, seperator)
        elif any(o in n for o in ["mp3", "wav"]) and not directory+seperator+n in found_songs:
            found_songs.append(directory+seperator+n)
    return found_songs
