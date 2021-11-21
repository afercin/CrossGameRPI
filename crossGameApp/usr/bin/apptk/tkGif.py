from apptk.tkAnimation import *
from PIL import Image, ImageTk as itk

class tkGif(tkAnimation):
    def __init__(self,
                 source=None,
                 autostart=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        if source is None:
            self.setSource("/usr/share/apptk/images/homer.gif", autostart)
        else:
            self.setSource(source, autostart)
    
    def setSource(self, source, autostart):
        if self.running:
            self.running = False
            
        self.source = source
        
        self.image = Image.open(self.source)
        self.reset()

        self.resize = self.image.width != self.width or self.image.height != self.height
        
        if self.resize:
            self.currentFrame = self.image.resize((self.width, self.height), Image.ANTIALIAS)
        else:
            self.currentFrame = self.image

        self.currentFrame = itk.PhotoImage(self.currentFrame)

        self.configure(image=self.currentFrame)

        self.frames = []
        self.frames.append(self.currentFrame)

        self.maxFrames = 1
        self.initialized = False

        if autostart:
            self.play()

    def getNextFrame(self):
        if self.initialized:
            self.i += 1
            if self.i < self.maxFrames:
                return self.frames[self.i]
        else:
            try:
                self.image.seek(self.image.tell()+1)
                
                if self.resize:
                    img = self.image.resize((self.width, self.height), Image.ANTIALIAS)
                else:
                    img = self.image

                img = itk.PhotoImage(img)

                if self.repeat:
                    self.frames.append(img)
                    self.maxFrames += 1

                return img
            except EOFError:
                if self.repeat:
                    self.initialized = True

        if self.repeat:
            self.reset()
            return self.getNextFrame()
        else:
            raise EndOfAnimation()
    
    def reset(self):
        if self.repeat:
            self.i = -1
        else:
            self.image = Image.open(self.source)