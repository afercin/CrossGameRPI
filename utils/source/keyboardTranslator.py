from pynput.keyboard import Controller, Key
from irDeconder import irDecoder
from controllerHook import *
import configparser
import requests
import os

CONFFILE = "/etc/productConf/cg.conf"
IP = "localhost"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameUtils" + CONFFILE
    IP = "10.0.0.20"

APIPATH = f"http://{IP}:5000/api/v1"

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
    # "TVPowerReleased": "TVPowerReleased",
    # "TVSourceReleased": "TVSourceReleased",
    # "TVVolumeUpReleased": "TVVolumeUpReleased",
    # "TVVolumeDownReleased": "TVVolumeDownReleased",
    # "TVMuteReleased": "TVMuteReleased",
    # "TVPower": "TVPower",
    "TIVO": "q",
    "Left": "a",
    "Up": "w",
    "Right": "d",
    "Down": "s",
    "Ok": Key.enter,
    # "TVSource": "TVSource",
    # "Language": "Language",
    # "Zoom": "Zoom",
    # "Guide": Key.home,
    # "Info": Key.end,
    # "ShowTV": "ShowTV",

    "TVVolumeUp": "+",
    "TVVolumeDown": "-",
    "TVMute": "mute",

    # "ProgUp": Key.page_up,
    # "ProgDown": Key.page_down,
    # "Dislike": "Dislike",
    # "Rec": "Rec",
    # "Like": "Like",

    "Play": Key.space,
    "Pause": Key.space,
    "Prev": Key.left,
    "Next": Key.right,
    "Back": "Back",
    # "Slow": "Slow",
    # "GoOn": "GoOn",
    # "Videoclub": "Videoclub",

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

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFFILE)

        self.controller = controllerHook(inactivityTime=self.config["DEFAULT"]["controllerInactivityTime"], verbose=True)
        self.controller.onKeyDown(self.checkControllerKeyDown)

        self.decoder = irDecoder(pin=int(self.config["DEFAULT"]["irPin"]))
        self.decoder.onDataReceived(self.checkDecoderDataReceived)

    def sendKey(self, key):
        if key == "powerOff":
            os.system("shutdown -f 0")
        elif key == "+":
            requests.get(f"{APIPATH}/system/audio/volume-up")
        elif key == "-":
            requests.get(f"{APIPATH}/system/audio/volume-down")
        elif key == "mute":
            requests.get(f"{APIPATH}/system/audio/toogle")
        elif key == "restartx":
            requests.get(f"{APIPATH}/system/restartx")
        elif key == "disconnect":
            for device in requests.get(f"{APIPATH}/system/bluetooth/devices").json():
                if device["name"] == "Wireless Controller":
                    requests.get(f"{APIPATH}/system/bluetooth/disconnect?device=A0:AB:51:03:21:8F")
                    break
        elif not os.path.isfile(self.config["CONTROL"]["emulator"]):
            self.keyboard = Controller()
            self.keyboard.press(key)
            self.keyboard.release(key)

    def checkControllerKeyDown(self, keyDown):
        if self.controller.button[controller.PS] and self.controller.button[controller.SELECT]:
            self.sendKey("powerOff")
        elif self.controller.button[controller.SELECT] and self.controller.button[controller.START]:
            self.sendKey("disconnect")
        elif self.controller.button[controller.PS] and self.controller.doublePress:
            self.sendKey("restartx")
        elif keyDown in DS4MAP.keys():
            self.sendKey(DS4MAP[keyDown])

    def checkDecoderDataReceived(self, keyDown):
        if keyDown == "Power":
            self.sendKey("powerOff")
        elif keyDown == "Back":
            self.sendKey("restartx")
            self.sendKey("Q")        
        elif os.path.isfile(self.config["CONTROL"]["tv"]):
            if keyDown == "ProgUp":
                requests.get(f"{APIPATH}/tv/channel-up")
            elif keyDown == "ProgDown":
                requests.get(f"{APIPATH}/tv/channel-down")
            else:
                try:
                    keyDown = int(keyDown)
                    requests.get(f"{APIPATH}/tv/channel?number={keyDown}")
                except:
                    pass
        elif keyDown in IRMAP.keys():
            self.sendKey(IRMAP[keyDown])

    def start(self):
        self.controller.start()
        self.decoder.start()

    def stop(self):
        self.controller.stop()
        self.decoder.stop()


if __name__ == "__main__":
    a = keyboardTranslator()
    a.start()
