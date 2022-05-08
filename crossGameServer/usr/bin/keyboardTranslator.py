import os
from pynput.keyboard import Controller, Key
from irDeconder import irDecoder
from controllerHook import *
from logUtils import logUtils
import requests

EMULATORCONTROL = "/tmp/emulator.mode"

DS4MAP = {
    controller.A: Key.enter,
    controller.O: "q",
    controller.Y: "y",
    controller.X: "x",
    # controller.LB: Key.f1,
    # controller.RB: Key.f2,
    # controller.LT: Key.f3,
    # controller.RT: Key.f4,
    controller.START: "r",
    controller.SELECT: "o",
    # controller.PS: Key.f6,
    # controller.L3: Key.f7,
    # controller.R3: Key.f8,
    controller.L_LEFT: "a",
    controller.L_UP: "w",
    controller.L_RIGHT: "d",
    controller.L_DOWN: "s",
    # controller.R_LEFT: Key.f9,
    # controller.R_UP: Key.page_up,
    # controller.R_RIGHT: Key.f10,
    # controller.R_DOWN: Key.page_down,
}

IRMAP = {
    #"0x3a10c0807": "TVPowerReleased",
    #"0x3a10c2c03": "TVSourceReleased",
    #"0x3a10cb807": "TVVolumeUpReleased",
    #"0x3a10c3807": "TVVolumeDownReleased",
    #"0x3a10cd807": "TVMuteReleased",
    #"0x320df10ef": "TVPower",
    "TIVO": "q",
    "Left": "a",
    "Up": "w",
    "Right": "d",
    "Down": "s",
    "Ok": Key.enter,
    #"0x320dfd02f": "TVSource",
    #"0x3a10c510e": "Language",
    #"0x3a10c220d": "Zoom",
    "Guide": Key.home,
    "Info": Key.end,
    #"0x3a10c8807": "ShowTV",

    #"0x320df40bf": "TVVolumeUp",
    #"0x320dfc03f": "TVVolumeDown",
    #"0x320df906f": "TVMute",

    "ProgUp": Key.page_up,
    "ProgDown": Key.page_down,
    # "0x3a10c1807": "Dislike",
    # "0x3a10c040b": "Rec",
    # "0x3a10c5807": "Like",

    # "0x3a10c840b": "Play",
    # "0x3a10cc40b": "Pause",
    # "0x3a10c440b": "Prev",
    # "0x3a10c240b": "Next",
    # "0x3a10c640b": "Back",
    # "0x3a10ca40b": "Slow",
    # "0x3a10ce40b": "GoOn",
    # "0x3a10cba05": "Videoclub",

    "Red": Key.f1,
    "Green": Key.f2,
    "Yellow": Key.f3,
    "Blue": Key.f3,
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    # "0x3a10c4c03": "C",
    "0": "0",
    "Enter": Key.backspace,
}


class keyboardTranslator():

    def __init__(self, verbose=False):

        self.controller = controllerHook(inactivityTime=15, verbose=True)
        self.controller.onKeyDown(self.checkControllerKeyDown)

        self.decoder = irDecoder(pin=12)
        self.decoder.onDataReceived(self.checkDecoderDataReceived)

        self.log = logUtils(verbose=verbose)

    def sendKey(self, key):
        if not os.path.isfile(EMULATORCONTROL):
            self.keyboard = Controller()
            self.keyboard.press(key)
            self.keyboard.release(key)

    def checkControllerKeyDown(self, keyDown):
        if self.controller.button[controller.PS] and self.controller.button[controller.SELECT]:
            self.log.info("Powering off")
            os.system("shutdown -f 0")
        if self.controller.button[controller.SELECT] and self.controller.button[controller.START]:
            self.log.info("Restarting X")
            os.system("/usr/bin/restartx")
        if self.controller.button[controller.PS] and self.controller.doublePress:
            self.log.info("Killing emulator process")
            requests.request("GET", "http://localhost:5000/api/v1/game/close")
        if keyDown in DS4MAP.keys():
            self.sendKey(DS4MAP[keyDown])

    def checkDecoderDataReceived(self, keyDown):
        if keyDown in IRMAP.keys():
            self.sendKey(IRMAP[keyDown])

    def start(self):
        self.log.info("starting")
        self.controller.start()
        self.decoder.start()

    def stop(self):
        self.log.info("stopping")
        self.controller.stop()
        self.decoder.stop()


if __name__ == "__main__":
    a = keyboardTranslator(verbose=True)
    a.start()
