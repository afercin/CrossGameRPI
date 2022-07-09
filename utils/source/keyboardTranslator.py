#!/usr/bin/python3
import os
from time import sleep

while not os.path.isfile("/tmp/display"):
    print("Waiting x11")
    sleep(1)

try:
    os.environ["DISPLAY"]
except:
    with open("/tmp/display") as f:
        os.environ["DISPLAY"] = f.readline().split()[0]

from pynput.keyboard import Controller, Key
from irDecoder import irDecoder
from controllerHook import *
import configparser
import requests

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
        confPath = "/etc/productConf"
        if "dev" in os.path.abspath(os.getcwd()):
            confPath = "/home/afercin/dev/CrossGameRPI/crossGameUtils" + confPath
        
        self.config = configparser.ConfigParser()
        self.config.read(f"{confPath}/translator.ini")

        control = configparser.ConfigParser()
        control.read(f"{confPath}/api.ini")

        if not self.config.has_section("API"):
            print("ERROR - Config has not section API.")
            os._exit(1)

        if not self.config.has_section("DS4MAP"):
            print("ERROR - Config has not section DS4MAP.")
            os._exit(2)
        
        if not control.has_section("CONTROL"):
            print("ERROR - Config has not section CONTROL.")
            os._exit(3)
        
        self.apiPath = self.config["API"]["path"]
        self.DS4MAP = self.config["DS4MAP"]

        self.config.add_section("CONTROL")
        self.config["CONTROL"] = control["CONTROL"]

        self.controller = controllerHook(verbose=True)
        self.controller.onKeyDown(self.checkControllerKeyDown)

        self.decoder = irDecoder()
        self.decoder.onDataReceived(self.checkDecoderDataReceived)

    def sendKey(self, key):
        if key == "powerOff":
            os.system("shutdown -f 0")
        elif key == "+":
            requests.get(f"{self.apiPath}/system/audio/volume-up")
        elif key == "-":
            requests.get(f"{self.apiPath}/system/audio/volume-down")
        elif key == "mute":
            requests.get(f"{self.apiPath}/system/audio/toogle")
        elif key == "restartx":
            requests.get(f"{self.apiPath}/system/restartx")
        elif key == "disconnect":
            for device in requests.get(f"{self.apiPath}/system/bluetooth/devices").json():
                if device["name"] == "Wireless Controller":
                    requests.get(f"{self.apiPath}/system/bluetooth/disconnect?device=A0:AB:51:03:21:8F")
                    break
        elif not os.path.isfile(self.config["CONTROL"]["emulator"]):
            self.keyboard = Controller()
            try:
                self.keyboard.press(eval(key))
                self.keyboard.release(eval(key))            
            except:
                self.keyboard.press(key)
                self.keyboard.release(key)

    def checkControllerKeyDown(self, keyDown):
        if self.controller.button[int(self.controller.buttons["ps"])] and self.controller.button[int(self.controller.buttons["select"])]:
            self.sendKey("powerOff")
        elif self.controller.button[int(self.controller.buttons["select"])] and self.controller.button[int(self.controller.buttons["start"])]:
            self.sendKey("disconnect")
        elif self.controller.button[int(self.controller.buttons["ps"])] and self.controller.doublePress:
            self.sendKey("restartx")
        elif keyDown in self.DS4MAP.keys():
            self.sendKey(self.DS4MAP[keyDown])

    def checkDecoderDataReceived(self, keyDown):
        if keyDown == "Power":
            self.sendKey("powerOff")
        elif keyDown == "Back":
            self.sendKey("restartx")
            self.sendKey("Q")        
        elif os.path.isfile(self.config["CONTROL"]["tv"]):
            if keyDown == "ProgUp":
                requests.get(f"{self.apiPath}/tv/channel-up")
            elif keyDown == "ProgDown":
                requests.get(f"{self.apiPath}/tv/channel-down")
            else:
                try:
                    keyDown = int(keyDown)
                    requests.get(f"{self.apiPath}/tv/channel?number={keyDown}")
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
