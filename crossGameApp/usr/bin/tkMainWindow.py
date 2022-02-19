import tkinter
import os
from apptk.tkOption import tkOption
from apptk.tkGameScreen import tkGameScreen
import pyautogui

if "dev" in os.path.dirname(os.path.abspath(__file__)):
    ROOTDIR = "/home/afercin/dev/CrossGameRPI/crossGameApp/"
    CURSOR = "hand2"
else:
    ROOTDIR = "/"
    CURSOR = "none"


class tkWindow(tkinter.Tk):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)

        from screeninfo import get_monitors
        for m in get_monitors():
            if m.x == 0 and m.y == 0:
                self.WIDTH = m.width
                self.HEIGHT = m.height

        self.attributes("-fullscreen", True)
        self.geometry(str(self.WIDTH) + "x" + str(self.HEIGHT))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<KeyPress>", self.keyPressed)
        self.bind("<Command-q>", self.on_closing)

        self.position = 0
        self.initializeControls()

    def keyPressed(self, key):
        if key.keysym == "Up":
            Popup(self)
        if key.keysym == "Left":
            self.position -= 1
            if self.position < 0:
                self.position = 2
            pyautogui.moveTo(
                self.positions[self.position] * self.WIDTH, self.startY * self.HEIGHT + 30)
        if key.keysym == "Right":
            self.position += 1
            if self.position > 2:
                self.position = 0
            pyautogui.moveTo(
                self.positions[self.position] * self.WIDTH, self.startY * self.HEIGHT + 30)
        if key.keysym in ("Return", "KP_Enter"):
            pyautogui.click()
        print(key.keysym)

    def initializeControls(self):
        self.mainWindow = tkinter.Canvas(
            self, width=self.WIDTH, height=self.HEIGHT, highlightthickness=0)
        self.mainWindow.place(x=0, y=0)

        self.startY = 0.05
        self.startX = 0.028125
        margin = self.HEIGHT * self.startY
        height = self.HEIGHT - margin * 2
        width = (self.WIDTH - margin * 4) / 3

        self.positions = (self.startX, 0.5, 0.5 +
                          (width / self.WIDTH) + self.startX)

        self.tv = tkOption(master=self.mainWindow,
                           image="{}rpi/apptk/videos/God of War.mp4".format(
                               ROOTDIR),
                           width=width,
                           height=height,
                           maxwidth=self.WIDTH,
                           maxheight=self.HEIGHT,
                           cursor=CURSOR,
                           command=lambda: self.tv.fullScreen(self.positions[0], self.startY, tkinter.NW))
        self.tv.place(relx=self.positions[0],
                      rely=self.startY,
                      anchor=tkinter.NW)

        self.games = tkOption(master=self.mainWindow,
                              image="{}rpi/apptk/videos/God of War.mp4".format(
                                  ROOTDIR),
                              width=width,
                              height=height,
                              maxwidth=self.WIDTH,
                              maxheight=self.HEIGHT,
                              cursor=CURSOR,
                              command=lambda: self.games.fullScreen(self.positions[1], self.startY, tkinter.N))
        self.games.place(relx=self.positions[1],
                         rely=self.startY,
                         anchor=tkinter.N)

        self.media = tkOption(master=self.mainWindow,
                              image="{}rpi/apptk/videos/God of War.mp4".format(
                                  ROOTDIR),
                              width=width,
                              height=height,
                              maxwidth=self.WIDTH,
                              maxheight=self.HEIGHT,
                              cursor=CURSOR,
                              command=lambda: self.media.fullScreen(self.positions[2], self.startY, tkinter.N))
        self.media.place(relx=self.positions[2],
                         rely=self.startY,
                         anchor=tkinter.N)
        pyautogui.moveTo(
            self.positions[0] * self.WIDTH + 30, self.startY * self.HEIGHT + 30)

    def on_closing(self, event=0):
        # self.controller.dispose()
        self.running = False
        self.destroy()
        exit()

    def start(self):
        self.running = True
        self.mainloop()


class Popup(tkinter.Toplevel):
    def __init__(self, master):
        tkinter.Toplevel.__init__(self, master)

        lbl = tkinter.Label(self, text="this is the popup")
        lbl.pack()

        btn = tkinter.Button(self, text="OK", command=self.destroy)
        btn.pack()

        self.transient(master)  # set to be on top of the main window
        self.grab_set()  # hijack all commands from the master (clicks on the main window are ignored)
        # pause anything on the main window until this one closes (optional)
        master.wait_window(self)


if __name__ == "__main__":
    app = tkWindow()
    app.start()
