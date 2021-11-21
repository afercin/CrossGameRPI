import pygame
import threading
import time
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
    LEFT = 13
    UP = 14  
    RIGHT = 15
    DOWN = 16

class controllerHook(Observer):
    def __init__(self, inactivityTime, verbose = False):
        pygame.init()
        Observer.__init__(self)
        
        self.log = logUtils(verbose=verbose)
        self.inactivityTime = inactivityTime
        self.verbose = verbose

        self.joysticks = []
        self.button=[False] * 17
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
                if self.KeyDown:
                    Event("OnKeyDown", buttonNumber)
                self.button[buttonNumber] = True
            else:
                if self.KeyUp:
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
            while self.pause:
                time.sleep(1)

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

            for event in pygame.event.get(eventtype=[1538,1539,1540]): #1536 joys and triggers
                if event.type == 1538:
                    x, y = event.value

                    if self.button[13] and x == 0:
                        sendKey(False, controller.LEFT)
                    elif self.button[14] and y == 0:
                        sendKey(False, controller.UP)
                    elif self.button[15] and x == 0:
                        sendKey(False, controller.RIGHT)
                    elif self.button[16] and y == 0:
                        sendKey(False, controller.DOWN)

                    if not self.button[13] and x == -1:
                        sendKey(True, controller.LEFT)
                    elif not self.button[14] and y == 1:
                        sendKey(True, controller.UP)
                    elif not self.button[15] and x == 1:
                        sendKey(True, controller.RIGHT)
                    elif not self.button[16] and y == -1:
                        sendKey(True, controller.DOWN)

                elif event.type in (1539, 1540):
                    sendKey(event.type == 1539, event.button)

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