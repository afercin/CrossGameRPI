from tkinter import *
import vlc
import os

class tkVideo(Frame):
    def __init__(self, 
                 width=800,
                 height=600,
                 source=None,
                 autostart=True,
                 repeat=False,
                 backcolor="black",
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.repeat = repeat

        self.canvas = Canvas(self, width=width, height=height, bg=backcolor, highlightthickness=0)
        self.canvas.pack()

        self.instance = vlc.Instance("--no-xlib")
        self.player = self.instance.media_player_new()
        self.player.set_xwindow(self.winfo_id())

        if source is None:
            self.setSource("/usr/share/apptk/videos/God of War – Story Trailer PS4.mp4", autostart)
        else:
            self.setSource(source, autostart)

    def setSource(self, source, autostart):
        if self.player.is_playing():
            self.stop()
            os.system('TASKKILL /F /IM VLC.EXE')

        self.source = source
        self.media = self.instance.media_new(self.source)
        self.media.get_mrl()
        self.player.set_media(self.media)

        if autostart:
            self.play()

    def stop(self):
        self.player.stop()

    def play(self):
        self.after(50, self.player.play)

    def reset(self):
        self.stop()
        self.play()

    def pause(self):
        self.player.pause()