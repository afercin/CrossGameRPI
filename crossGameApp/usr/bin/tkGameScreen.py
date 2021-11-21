import tkinter
import glob
import os
from tkinter.constants import NW
from PIL import Image, ImageTk as itk
from tkVideo import tkVideo

class tkGameScreen(tkinter.Canvas):
    PAD_X = 50
    PAD_Y = 50
    TEXT_PX = 30
    TEXT_PY = 20

    COLOR_FACTOR = 2.5

    APP_PATH = "/usr/share/apptk/"

    def __init__(self, master):
        super().__init__(master, width=master.WIDTH, height=master.HEIGHT, highlightthickness=0)

        self.WIDTH = master.WIDTH
        self.HEIGHT = master.HEIGHT
        self.videoW = self.WIDTH / 2
        self.videoH = self.HEIGHT / 2

        self.TEXT_X = 0
        self.TEXT_Y = self.HEIGHT - self.videoH - self.PAD_Y * 2
        self.TEXT_W = self.WIDTH - self.videoW - self.TEXT_PX * 2 - self.PAD_X * 3
        self.TEXT_H = self.videoH - self.TEXT_PY * 2
        
        self.defaultImage = Image.open(self.APP_PATH + "images/God of War.jpg").resize([self.WIDTH, self.HEIGHT], Image.ANTIALIAS)
        
        self.bgImage = self.create_image(0,
                                         0,
                                         image=itk.PhotoImage(self.defaultImage),
                                         anchor=NW)
        self.text = [self.create_image(self.PAD_X + self.TEXT_X,
                                       self.PAD_Y + self.TEXT_Y,
                                       image=None,
                                       anchor=NW),
                     self.create_text(self.PAD_X + self.TEXT_X + self.TEXT_PX,
                                      self.PAD_Y +self.TEXT_Y + self.TEXT_PY,
                                      text="",
                                      anchor=NW,
                                      width=self.TEXT_W,
                                      fill="#fff")]
        self.video = None

    def setGame(self, name):
        self.image = self.defaultImage

        def setBg(source):
            files = glob.glob(source)
            if len(files) > 0:
                self.image = Image.open(files[0]).resize([self.WIDTH, self.HEIGHT], Image.ANTIALIAS)
            
            self.bg = itk.PhotoImage(self.image)
            self.itemconfig(self.bgImage, image=self.bg)
        
        def setText(source):
            self.textImage = None
            text = ""

            if os.path.isfile(source):
                with open(source) as f:
                    lines = f.readlines()
                for line in lines:
                    text += line

                img = self.image.crop((self.PAD_X + self.TEXT_X,
                                       self.PAD_Y + self.TEXT_Y,
                                       self.PAD_X + self.TEXT_X + self.TEXT_W + self.TEXT_PX * 2, 
                                       self.PAD_Y + self.TEXT_Y + self.TEXT_H + self.TEXT_PY * 2))
                pixels = []
                
                for r, g, b in img.getdata():
                    r /= self.COLOR_FACTOR
                    g /= self.COLOR_FACTOR
                    b /= self.COLOR_FACTOR
                    pixels.append((int(r), int(g), int(b)))

                img = Image.new(img.mode,img.size)
                img.putdata(pixels)
                self.textImage = itk.PhotoImage(img)
            self.itemconfig(self.text[0], image=self.textImage)
            self.itemconfig(self.text[1], text=text)
        
        def setVideo(source):
            files = glob.glob(source)
            if len(files) > 0:
                self.video = tkVideo(master=self, width=self.videoW, height=self.videoH, source=files[0])
                self.video.place(x = self.WIDTH - self.videoW - self.PAD_X, 
                                 y = self.HEIGHT - self.videoH - self.PAD_Y)
            elif self.video is not None:
                self.video.dispose()
        
        setBg(self.APP_PATH + "images/" + name + ".*")
        setText(self.APP_PATH + "texts/" + name + ".txt")
        setVideo(self.APP_PATH + "videos/" + name + ".*")