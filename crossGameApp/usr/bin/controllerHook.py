import pygame
import threading
import time
import os
from logUtils import logUtils 
from datetime import datetime
from event import *

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
    def __init__(self, inactivityTime, verbose = False):
        pygame.init()
        Observer.__init__(self)
        
        self.log = logUtils(verbose=verbose)
        self.inactivityTime = inactivityTime
        self.verbose = verbose

        self.joysticks = []
        self.button=[False] * 21
        self.deadzone=0.3

        self.KeyDown = None
        self.KeyUp = None
        self.end = True

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
                if self.KeyDown and not self.pause:
                    Event("OnKeyDown", buttonNumber)
                self.button[buttonNumber] = True
                if self.button[controller.START] and self.button[controller.SELECT]:
                    os.system("shutdown -f 0")
                if self.button[controller.SELECT] and self.button[controller.PS]:
                    os.system("restartx")
            else:
                if self.KeyUp and not self.pause:
                    Event("OnKeyUp", buttonNumber)
                self.button[buttonNumber] = False
            self.lastInput = datetime.now()

        def checkController():
            pygame.joystick.quit()
            pygame.joystick.init()
            if pygame.joystick.get_init():
                if len(self.joysticks) < pygame.joystick.get_count():
                    for i in range(len(self.joysticks), pygame.joystick.get_count()):
                        self.joysticks.append(pygame.joystick.Joystick(i))
                        self.log.info("Controller \"{}\" added in slot {}!".format(self.joysticks[i].get_name(), i))
                else:
                    joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
                    if len(self.joysticks) > len(joysticks):
                        self.log.warning("Controller disconected! Remaining controllers: {}".format(str(pygame.joystick.get_count())))
                    elif pygame.joystick.get_count() > 0:
                        self.log.info("Controller remaining connected!")
                    self.joysticks = joysticks
                                     
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
                    self.log.warning("Inactivity check...")
                checkController()
                time.sleep(0.05 if len(self.joysticks) == 0 else 0)
            
            show = False

            for event in pygame.event.get(eventtype=[1538,1539,1540,1536]): #1536 joys and triggers
                if event.type == 1538:
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

                elif event.type in (1539, 1540):
                    sendKey(event.type == 1539, event.button)
                else:
                    deadzone = 0.4
                    key=""
                    if event.axis in (0,1,3,4): # L=1,2; R=3,4; LT=2; RT=5
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
                            
            time.sleep(0.05)

if __name__ == "__main__":
    aaa = controllerHook(inactivityTime=15, verbose=True)

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