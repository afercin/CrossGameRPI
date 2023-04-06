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

        if not self.config.has_section("IRMAP"):
            print("ERROR - Config has not section IRMAP.")
            os._exit(3)
        
        if not control.has_section("CONTROL"):
            print("ERROR - Config has not section CONTROL.")
            os._exit(4)
        
        self.apiPath = self.config["API"]["path"]
        self.DS4MAP = self.config["DS4MAP"]
        self.IRMAP = self.config["IRMAP"]

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
        elif keyDown in self.IRMAP.keys():
            self.sendKey(self.IRMAP[keyDown])

    def start(self):
        self.controller.start()
        self.decoder.start()

    def stop(self):
        self.controller.stop()
        self.decoder.stop()


if __name__ == "__main__":
    a = keyboardTranslator()
    a.start()
