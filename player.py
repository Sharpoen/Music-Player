import vlc

class player:
    def __init__(self):
        self.player = vlc.MediaPlayer()
        self.state = "stopped"
    def loadPath(self, songPath):
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
    def stop(self):
        self.state="stopped"
        self.player.stop()
    def jumpTo(self, percentage):
        self.player.set_position(percentage/100)
    def set_volume(self, volume):
        self.player.audio_set_volume(volume)