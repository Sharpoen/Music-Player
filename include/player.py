import vlc

class audioPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.state = "stopped"
        self.song_table = None
        self.new_cover = False
    def exit(self):
        self.stop()
    def check_cover(self):
        if self.new_cover:
            self.new_cover=False
            return True
        else: return False
    def loadPath(self, songPath:str):
        if type(songPath)!=str: return
        self.player.stop()
        self.player.set_media(vlc.Media(songPath))
        if self.state=="playing":
            self.player.play()
        else:
            self.state="stopped"
    def playToggle(self):
        if self.state=="playing":
            self.state="paused"
            self.player.pause()
        else:
            self.state="playing"
            self.player.play()
    def next(self):
        if self.song_table:
            self.loadPath(self.song_table.next())
    def previous(self):
        seconds = self.player.get_time()/1000
        if self.song_table and seconds<=2: self.loadPath(self.song_table.previous())
        else: self.jumpTo(0)
    def stop(self):
        self.state="stopped"
        self.player.stop()
    def jumpTo(self, percentage):
        self.player.set_position(percentage/100)
    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

if __name__ == "__main__":
    print("Testing Audio Player")
    test = audioPlayer()