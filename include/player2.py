import vlc

class audioPlayer:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.state = "stopped"
        self.new_cover = False
    def exit(self):
        self.stop()
    def check_cover(self):
        if self.new_cover:
            self.new_cover=False
            return True
        else: return False
    def load(self, path:str):
        if type(path)!=str: return
        self.player.stop()
        self.player.set_media(vlc.Media(path))
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
    def stop(self):
        self.state="stopped"
        self.player.stop()
    def goto(self, pos : float):
        self.player.set_position(pos)
    def set_volume(self, volume):
        self.player.audio_set_volume(int(volume))

if __name__ == "__main__":
    print("Testing Audio Player")
    test = audioPlayer()