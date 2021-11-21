import tkinter
from abc import ABC

class EndOfAnimation(Exception):
    pass

class tkAnimation(tkinter.Label, ABC):
    def __init__(self,
                 width=400,
                 height=300,
                 delay=50,
                 repeat=True,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.width = width
        self.height = height
        self.repeat = repeat
        self.running = False
        self.delay = delay
        self.ended = False

        self.configure(width=self.width, height=self.height)

    def play(self):
        if not self.running:
            self.currentFrame = 1
            self.running = True
            if self.ended:
                self.reset()
                self.ended = False
            self.beginAnimation()

    def pause(self):
        if self.running:
            self.running = False

    def stop(self):
        if self.running:
            self.running = False
            self.reset()
    
    def setSource(self, source, autostart):
        raise NotImplementedError()

    def getNextFrame(self):
        raise NotImplementedError()

    def reset(self):
        raise NotImplementedError()
    
    def beginAnimation(self):
        try:
            if self.running:
                nextFrame = self.getNextFrame()
                self.configure(image=nextFrame)
                self.currentFrame = nextFrame
                self.after(self.delay, func=self.beginAnimation)

        except EndOfAnimation:
            self.running = False
            self.ended = True

        except Exception as e:
            print(str(e))