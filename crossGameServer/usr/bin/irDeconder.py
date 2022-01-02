import RPi.GPIO as GPIO
import multiprocessing
from datetime import datetime
from logUtils import logUtils
from event import *


class irDecoder(Observer):

    def __init__(self, pin, verbose=False):
        Observer.__init__(self)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin, GPIO.IN)

        self.log = logUtils(verbose=verbose)
        self.pin = pin
        self.end = True

    def dispose(self):
        if not self.end:
            self.stop()
        self.log.dispose()

    def start(self):
        if self.end:
            self.log.info("Initializeing IR decoder...")
            self.end = False
            self.pause = False
            self.checkInputThread = multiprocessing.Process(
                target=self.checkInData)
            self.log.info("IR decoder initialized")
            self.checkInputThread.start()

    def stop(self):
        self.end = True
        self.log.info("Stopping IR decoder...")
        if not self.checkInputThread.join(1):
            self.checkInputThread.terminate()
        self.log.info("IR decoder stopped!")

    def onDataReceived(self, eventHandler):
        self.dataReceived = True
        self.observe("OnDataReceived", eventHandler)

    def checkInData(self):
        BUTTONS = {
            "0x300ffa25d": "1",
            "0x300ff629d": "2",
            "0x300ffe21d": "3",
            "0x300ff22dd": "4",
            "0x300ff02fd": "5",
            "0x300ffc23d": "6",
            "0x300ffe01f": "7",
            "0x300ffa857": "8",
            "0x300ff906f": "9",
            "0x300ff9867": "0",
            "0x300ff6897": "*",
            "0x300ffb04f": "#",
            "0x300ff10ef": "Left",
            "0x300ff18e7": "Up",
            "0x300ff4ab5": "Down",
            "0x300ff5aa5": "Right",
            "0x300ff38c7": "Enter"
        }
        while not self.end:
            inData = self.getInData()
            if inData not in ("0x1", "0x3", "0x5"):
                if self.dataReceived:
                    if inData in BUTTONS.keys():
                        Event("OnDataReceived", BUTTONS[inData])
                    else:
                        self.log.error("Unknow value \"{}\"!".format(inData))

    def getInData(self):
        def convertHex(binaryValue):
            tmpB2 = int(str(binaryValue), 2)  # Tempary propper base 2
            return hex(tmpB2)

        # Internal vars
        num1s = 0  # Number of consecutive 1s read
        binary = 1  # The bianry value
        command = []  # The list to store pulse times in
        previousValue = 0  # The last value
        value = GPIO.input(self.pin)  # The current value

        # Waits for the sensor to pull pin low
        while value:
            value = GPIO.input(self.pin)
        # Records start time
        startTime = datetime.now()

        while num1s <= 10000 and not self.end:
            # If change detected in value
            if previousValue != value:
                now = datetime.now()
                pulseTime = now - startTime
                startTime = now
                # Store recorded data
                command.append((previousValue, pulseTime.microseconds))

            # Updates consecutive 1s variable
            if value:
                num1s += 1
            else:
                num1s = 0

            if num1s <= 10000:
                previousValue = value
                value = GPIO.input(self.pin)

        # Converts times to binary
        for (type, time) in command:
            if type == 1:
                if time > 1000:  # If pulse greater than 1000us
                    binary = binary * 10 + 1  # Must be 1
                else:
                    binary *= 10  # Must be 0

        if len(str(binary)) > 34:  # Sometimes, there is some stray characters
            binary = int(str(binary)[:34])

        return convertHex(binary)


if __name__ == "__main__":
    def valueReceived(value):
        print("Received value: {}".format(value))
    ir = irDecoder(pin=12, verbose=True)
    ir.onDataReceived(valueReceived)
    ir.start()
    input()
    ir.stop()
