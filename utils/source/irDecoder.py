import RPi.GPIO as GPIO
import multiprocessing
from datetime import datetime
from logUtils import logUtils
from event import *


class irDecoder(Observer):

    BUTTONS = {
        "0x3a10c0807": "TVPowerReleased",
        "0x3a10c2c03": "TVSourceReleased",
        "0x3a10cb807": "TVVolumeUpReleased",
        "0x3a10c3807": "TVVolumeDownReleased",
        "0x3a10cd807": "TVMuteReleased",

        "0x320df10ef": "TVPower",
        "0x3a10c700f": "TIVO",
        "0x3a10cd10e": "Power",
        "0x3a10c2807": "Up",
        "0x3a10c6807": "Down",
        "0x3a10ce807": "Left",
        "0x3a10ca807": "Right",
        "0x3a10c9807": "Ok",
        "0x320dfd02f": "TVSource",
        "0x3a10c510e": "Language",
        "0x3a10c220d": "Zoom",
        "0x3a10c6c03": "Guide",
        "0x3a10cc807": "Info",
        "0x3a10c8807": "ShowTV",

        "0x320df40bf": "TVVolumeUp",
        "0x320dfc03f": "TVVolumeDown",
        "0x320df906f": "TVMute",
        "0x3a10c7807": "ProgUp",
        "0x3a10cf807": "ProgDown",
        "0x3a10c1807": "Dislike",
        "0x3a10c040b": "Rec",
        "0x3a10c5807": "Like",

        "0x3a10c840b": "Play",
        "0x3a10cc40b": "Pause",
        "0x3a10c440b": "Prev",
        "0x3a10c240b": "Next",
        "0x3a10c640b": "Back",
        "0x3a10ca40b": "Slow",
        "0x3a10ce40b": "GoOn",
        "0x3a10cba05": "Videoclub",

        "0x3a10c0609": "Red",
        "0x3a10c8609": "Green",
        "0x3a10c4609": "Yellow",
        "0x3a10cc609": "Blue",
        "0x3a10c140b": "1",
        "0x3a10c940b": "2",
        "0x3a10c540b": "3",
        "0x3a10cd40b": "4",
        "0x3a10c340b": "5",
        "0x3a10cb40b": "6",
        "0x3a10c740b": "7",
        "0x3a10cf40b": "8",
        "0x3a10c0c03": "9",
        "0x3a10c4c03": "C",
        "0x3a10c8c03": "0",
        "0x3a10ccc03": "Enter"
    }

    TRASH = ["0x1", "0x2", "0x3", "0x4", "0x5"]

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
        while not self.end:
            inData = self.getInData()
            if inData not in self.TRASH:
                if self.dataReceived:
                    if inData in self.BUTTONS.keys():
                        Event("OnDataReceived", self.BUTTONS[inData])
                    else:
                        self.log.error(
                            "Unknow value \"{}\"!".format(inData))

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
