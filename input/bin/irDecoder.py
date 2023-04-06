from datetime import datetime
from event import *
import RPi.GPIO as GPIO
import multiprocessing
import configparser
import atexit
import logger
import os


class irDecoder(Observer):
    def __init__(self, verbose=False):
        Observer.__init__(self)

        configFile = "/etc/productConf/irDecoder.ini"
        if "dev" in os.path.abspath(os.getcwd()):
            configFile = "/home/adrix/personal_dev/CrossGameRPI/utils" + configFile

        config = configparser.ConfigParser()
        config.read(configFile)

        self.log = logger.start_logger(config, verbose)
        atexit.register(self.log.printTail)

        if not config.has_section("DECODER"):
            print("ERROR - Config has not section DECODER.")
            os._exit(1)

        if not config.has_section("BUTTONS"):
            print("ERROR - Config has not section BUTTONS.")
            os._exit(2)

        if not config.has_section("UNKNOW"):
            print("ERROR - Config has not section UNKNOW.")
            os._exit(3)
        
        self.pin = int(config["DECODER"]["pin"])
        self.buttons = config["BUTTONS"]

        self.trash = list()
        for trashSignal in config["UNKNOW"]["trash"].split(";"):
            self.trash.append(trashSignal)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.IN)

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
            if inData not in self.trash:
                if self.dataReceived:
                    if inData in self.buttons.keys():
                        Event("OnDataReceived", self.buttons[inData])
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
    ir = irDecoder(verbose=True)
    ir.onDataReceived(valueReceived)
    ir.start()
    input()
    ir.stop()
