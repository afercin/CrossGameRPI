from apptk.tkAnimation import *
from PIL import Image, ImageTk as itk
import cv2
import imutils

class IncompatibleFormat(Exception):
    pass

class tkVideoCV(tkAnimation):
    def __init__(self,
                 source=None,
                 autostart=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if source is None:
            self.setSource("/usr/shate/apptk/videos/God of War – Story Trailer PS4.mp4", autostart)
        else:
            self.setSource(source, autostart)
    
    def setSource(self, source, autostart):
        if self.running:
            self.running = False

        self.source = source

        self.video = cv2.VideoCapture(source)
        ret, frame = self.video.read()

        if ret:
            self.resize = frame.shape[0] != self.width or frame.shape[1] != self.height

            self.reset()

            if autostart:
                self.play()
        else:
            raise IncompatibleFormat()
        

    def getNextFrame(self):
        ret, frame = self.video.read()
        if ret == True:
            if self.resize:
                frame = imutils.resize(frame, width=self.width, height=self.height)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return itk.PhotoImage(Image.fromarray(frame))
        else:
            if self.repeat:
                self.reset()
                return self.getNextFrame()
            else:
                self.video.release()
                raise EndOfAnimation()
    
    def reset(self):
        self.video.release()
        self.video = cv2.VideoCapture(self.source)