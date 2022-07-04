#!/usr/bin/python3
from datetime import datetime
from event import *
import configparser
import lsb_release
import threading
import atexit
import pygame
import logger
import time
import os


class controller:
    A = 0
    O = 1
    Y = 2
    X = 3
    LB = 4
    RB = 5
    LT = 6
    RT = 7
    SELECT = 8
    START = 9
    PS = 10
    L3 = 11
    R3 = 12
    L_LEFT = 13
    L_UP = 14
    L_RIGHT = 15
    L_DOWN = 16
    R_LEFT = 17
    R_UP = 18
    R_RIGHT = 19
    R_DOWN = 20


class controllerHook(Observer):
    def __init__(self, verbose=False):
        pygame.init()
        Observer.__init__(self)

        configFile = "/etc/productConf/controller.ini"
        if "dev" in os.path.abspath(os.getcwd()):
            configFile = "/home/adrix/personal_dev/CrossGameRPI/utils" + configFile

        config = configparser.ConfigParser()
        config.read(configFile)

        self.log = logger.start_logger(config, verbose)
        atexit.register(self.log.printTail)

        distro = lsb_release.get_distro_information()["ID"].upper()
        if not config.has_section(distro):
            print("ERROR - Linux distribution not supported.")
            os._exit(1)
        
        self.axis = int(config[distro]["axis"])
        self.dPad = int(config[distro]["dpad"])
        self.buttonDown = int(config[distro]["button_down"])
        self.buttonUp = int(config[distro]["button_up"])

        if not config.has_section("CONTROLLER"):
            print("ERROR - Config has not section CONTROLLER.")
            os._exit(2)

        self.inactivityTime = float(config["CONTROLLER"]["inactivity_time"])
        self.verbose = verbose

        self.joysticks = []
        self.button = [False] * 21
        self.deadzone = 0.3

        self.KeyDown = None
        self.KeyUp = None
        self.end = True
        self.doublePress = False
        self.lastKeyPressed = None


    def dispose(self):
        if not self.end:
            self.stop()
        self.log.dispose()

    def onKeyDown(self, eventHandler):
        self.KeyDown = True
        self.observe("OnKeyDown", eventHandler)

    def onKeyUp(self, eventHandler):
        self.KeyUp = True
        self.observe("OnKeyUp", eventHandler)

    def start(self):
        if self.end:
            self.log.info("Initializeing Hook...")
            self.end = False
            self.pause = False
            self.checkInputThread = threading.Thread(target=self.checkInputs)
            self.log.info("Hook initialized")
            self.checkInputThread.start()

    def stop(self):
        self.log.info("Clossing Hook...")
        self.end = True
        self.pause = False
        self.checkInputThread.join()
        self.log.info("Hook closed")

    def controllerConnected(self):
        return len(self.joysticks) > 0

    def pauseHook(self):
        self.log.info("Pausing Hook...")
        self.pause = True

    def resumeHook(self):
        self.log.info("Resumming Hook...")
        self.pause = False

    def checkInputs(self):
        def sendKey(pressed, buttonNumber):
            if pressed:
                self.button[buttonNumber] = True
                self.doublePress = self.lastKeyPressed == buttonNumber and (
                    datetime.now() - self.lastInput).total_seconds() < 0.15
                self.lastKeyPressed = buttonNumber
                if self.KeyDown and not self.pause:
                    Event("OnKeyDown", buttonNumber)
            else:
                self.button[buttonNumber] = False
                if self.KeyUp and not self.pause:
                    Event("OnKeyUp", buttonNumber)
            self.lastInput = datetime.now()

        def checkController():
            pygame.joystick.quit()
            pygame.joystick.init()
            if pygame.joystick.get_init():
                if len(self.joysticks) < pygame.joystick.get_count():
                    for i in range(len(self.joysticks), pygame.joystick.get_count()):
                        self.joysticks.append(pygame.joystick.Joystick(i))
                        name = str(self.joysticks[i].get_name())
                        self.log.info(
                            "Controller \"{}\" added in slot {}!".format(name, i))

                else:
                    joysticks = [pygame.joystick.Joystick(
                        i) for i in range(pygame.joystick.get_count())]
                    if len(self.joysticks) > len(joysticks):
                        self.log.warn("Controller disconected! Remaining controllers: {}".format(
                            str(pygame.joystick.get_count())))
                    elif pygame.joystick.get_count() > 0:
                        self.log.info("Controller remaining connected!")
                    self.joysticks = joysticks

                for joystick in self.joysticks:
                    joystick.init()
                self.lastInput = datetime.now()

        self.lastInput = datetime.now()
        show = False
        while not self.end:
            while len(self.joysticks) == 0 or (datetime.now() - self.lastInput).total_seconds() >= self.inactivityTime:
                if len(self.joysticks) == 0:
                    if not show:
                        self.log.info("Waiting for controller...")
                        show = True
                else:
                    self.log.warn("Inactivity check...")
                checkController()
                time.sleep(0.05 if len(self.joysticks) == 0 else 0)

            show = False

            # 1536 joys and triggers
            for event in pygame.event.get(eventtype=(self.axis, self.dPad, self.buttonDown, self.buttonUp)):
                if event.type == self.dPad:
                    x, y = event.value

                    if self.button[13] and x == 0:
                        sendKey(False, controller.L_LEFT)
                    elif self.button[14] and y == 0:
                        sendKey(False, controller.L_UP)
                    elif self.button[15] and x == 0:
                        sendKey(False, controller.L_RIGHT)
                    elif self.button[16] and y == 0:
                        sendKey(False, controller.L_DOWN)

                    if not self.button[13] and x == -1:
                        sendKey(True, controller.L_LEFT)
                    elif not self.button[14] and y == 1:
                        sendKey(True, controller.L_UP)
                    elif not self.button[15] and x == 1:
                        sendKey(True, controller.L_RIGHT)
                    elif not self.button[16] and y == -1:
                        sendKey(True, controller.L_DOWN)
                elif event.type == self.axis:
                    deadzone = 0.4
                    key = ""
                    # L=1,2; R=3,4; LT=2; RT=5
                    if event.axis in (0, 1, 3, 4):
                        if event.axis == 0:
                            key = controller.L_LEFT if event.value < 0 else controller.L_RIGHT
                        elif event.axis == 1:
                            key = controller.L_UP if event.value < 0 else controller.L_DOWN
                        if event.axis == 3:
                            key = controller.R_LEFT if event.value < 0 else controller.R_RIGHT
                        elif event.axis == 4:
                            key = controller.R_UP if event.value < 0 else controller.R_DOWN

                        if event.value > deadzone or event.value < -deadzone:
                            if not self.button[key]:
                                sendKey(True, key)
                        else:
                            if self.button[key]:
                                sendKey(False, key)
                elif event.type in (self.buttonDown, self.buttonUp):
                    sendKey(event.type == self.buttonDown, event.button)

            time.sleep(0.05)


if __name__ == "__main__":
    aaa = controllerHook(verbose=True)

    def keyUp(key):
        print("KeyUp: " + str(key))

    def keyDown(key):
        print("KeyDown: " + str(key))

    aaa.onKeyDown(keyDown)
    aaa.onKeyUp(keyUp)
    aaa.start()
    input()
    aaa.pauseHook()
    input()
    aaa.resumeHook()
    input()
    aaa.dispose()
