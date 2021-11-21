import tkinter
from tkVideo import tkVideo
from tkGif import tkGif
from tkButtom import tkButton
from tkGameScreen import tkGameScreen
from controllerHook import *

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

        self.controller = controllerHook(15)
        self.controller.onKeyUp(self.keyPressed)
        self.controller.start() 

        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.bind("<Command-q>", self.on_closing)
        self.bind("<Command-w>", self.on_closing)

        self.mode = 1
        self.canvas = None
        self.initializeControls()
        
    def keyPressed(self, key=None):
        if self.mode == 1:
            self.mode = 2
            self.canvas2.place_forget()
            if self.canvas is None:
                self.gameTest()
            else:
                self.canvas.place(x=0, y=0)
        else:
            self.mode = 1
            self.canvas.place_forget()
            self.canvas2.place(x=0, y=0)

    def gameTest(self):
        self.canvas = tkGameScreen(self)
        self.canvas.place(x=0, y=0)
        self.canvas.setGame("God of War")
    
    def initializeControls(self):
        self.canvas2 = tkinter.Canvas(self, width=self.WIDTH, height=self.HEIGHT, highlightthickness = 0)
        self.canvas2.place(x=0, y=0)
        def exampleButtons():

            # ========== slightly rounded corners =============

            """button_1 = tkVideo(master=self, 
                               width=1280, 
                               height=720)
            button_1.place(relx=0.33, rely=0.2, anchor=tkinter.CENTER)"""

            button_2 = tkButton(master=self.canvas2,
                                    bg_color=None,
                                    fg_color="#922B21",
                                    border_color="white",
                                    hover_color="#CD6155",
                                    text_font=None,
                                    text="Test Button 2",
                                    text_color="white",
                                    corner_radius=10,
                                    border_width=2,
                                    width=150,
                                    height=45,
                                    hover=True,
                                    cursor="hand2",
                                    command=self.keyPressed)
            button_2.place(relx=0.66, rely=0.2, anchor=tkinter.CENTER)

            # ========== fully rounded corners =============

            button_3 = tkButton(master=self.canvas2,
                                                bg_color=None,
                                                fg_color="#1E8449",
                                                hover_color="#2ECC71",
                                                text_font=None,
                                                text="Test Button 3",
                                                text_color="white",
                                                corner_radius=20,
                                                width=120,
                                                height=40,
                                                hover=True,
                                                cursor="hand2")
            button_3.place(relx=0.33, rely=0.4, anchor=tkinter.CENTER)

            button_4 = tkButton(master=self.canvas2,
                                                bg_color=None,
                                                border_color="#BB8FCE",
                                                fg_color="#6C3483",
                                                hover_color="#A569BD",
                                                text_font=None,
                                                text="Test Button 4",
                                                text_color="white",
                                                corner_radius=20,
                                                border_width=2,
                                                width=150,
                                                height=40,
                                                hover=True,
                                                cursor="hand2",
                                                command=button_7.stop)
            button_4.place(relx=0.66, rely=0.4, anchor=tkinter.CENTER)

            # ========== no rounded corners =============

            button_5 = tkButton(master=self.canvas2,
                                                bg_color=None,
                                                fg_color="#A93226",
                                                hover_color="#CD6155",
                                                text_font=None,
                                                text="Test Button 5",
                                                text_color="black",
                                                corner_radius=0,
                                                width=120,
                                                height=40,
                                                hover=True,
                                                cursor="hand2",
                                                command=button_7.reset)
            button_5.place(relx=0.33, rely=0.6, anchor=tkinter.CENTER)

            button_6 = tkButton(master=self.canvas2,
                                                bg_color=None,
                                                fg_color=self.cget("bg"),
                                                border_color="#ABB2B9",
                                                hover_color="#566573",
                                                text_font=None,
                                                text="Test Button 6",
                                                text_color="#ABB2B9",
                                                corner_radius=0,
                                                border_width=2,
                                                width=120,
                                                height=40,
                                                hover=True,
                                                cursor="hand2",
                                                command=button_7.play)
            button_6.place(relx=0.66, rely=0.6, anchor=tkinter.CENTER)

        
        # ========== other shapes =============
        try:
            button_7 = tkGif(master=self.canvas2, source="/usr/share/apptk/images/ZYZy.gif")
            button_7.place(relx=0.33, rely=0.8, anchor=tkinter.CENTER)

            button_8 = tkButton(master=self.canvas2,
                                                bg_color=None,
                                                fg_color="#212F3D",
                                                border_color="#117A65",
                                                hover_color="#34495E",
                                                text_font=None,
                                                text="Button 8",
                                                text_color="white",
                                                corner_radius=12,
                                                border_width=4,
                                                width=100,
                                                height=60,
                                                hover=True,
                                                cursor="hand2",
                                                command=button_7.pause)
            button_8.place(relx=0.66, rely=0.8, anchor=tkinter.CENTER)
            
            exampleButtons()
            
            self.running = False
        except Exception as e:
            print(str(e))

    def on_closing(self, event=0):
        self.controller.dispose()
        self.running = False
        self.destroy()
        exit()

    def start(self):
        self.running = True
        self.mainloop()

if __name__ == "__main__":
    app = tkWindow()
    app.start()