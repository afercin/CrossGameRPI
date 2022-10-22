#!/usr/bin/env python3
import tkinter

class tkWindow(tkinter.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, geometry, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        #self.attributes("-fullscreen", True)
        self.geometry(geometry)
        self.config(cursor="none")

        self.WIDTH = geometry.split("x")[0]
        self.HEIGHT = geometry.split("x")[1]

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<KeyPress>", self.on_closing)

        self.mainWindow = tkinter.Canvas(
            self, width=self.WIDTH, height=self.HEIGHT, highlightthickness=0, background="#000")
        self.mainWindow.place(x=0, y=0)

    def on_closing(self, event=0):
        # self.controller.dispose()
        self.running = False
        self.destroy()
        exit()

    def start(self):
        self.running = True
        self.mainloop()


if __name__ == "__main__":
    app = tkWindow("1920x1080")
    app.start()
