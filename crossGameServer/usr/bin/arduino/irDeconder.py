import RPi.GPIO as GPIO
import os
#from pynput.keyboard import Controller, Key
from datetime import datetime

# Static program vars
pin = 12  # Input pin of sensor (GPIO.BOARD)
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
    # "0x300ff10ef": Key.Left,
    # "0x300ff18e7": Key.Up,
    # "0x300ff4ab5": Key.Down,
    # "0x300ff5aa5": Key.Right,
    # "0x300ff38c7": Key.Enter
    "0x300ff10ef": "Left",
    "0x300ff18e7": "Up",
    "0x300ff4ab5": "Down",
    "0x300ff5aa5": "Right",
    "0x300ff38c7": "Enter"
}
# Buttons = [0x300ff9867, 0x300ffd827, 0x300ff8877, 0x300ffa857, 0x300ffe817, 0x300ff48b7, 0x300ff6897, 0x300ff02fd, 0x300ff32cd, 0x300ff20df] #HEX code list
# ButtonsNames = ["RED",   "GREEN",      "BLUE",       "WHITE",      "DARK ORANGE","LIGHT GREEN","DARK BLUE",  "VIBRANT ORANGE","LIGHT BLUE","DARK PURPLE"] #String list in same order as HEX list

# Sets up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)

# Gets binary value


def getBinary():
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The bianry value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = GPIO.input(pin)  # The current value

    # Waits for the sensor to pull pin low
    while value:
        value = GPIO.input(pin)
    # Records start time
    startTime = datetime.now()

    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            # Store recorded data
            command.append((previousValue, pulseTime.microseconds))

        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0

        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)

    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])

    return binary

# Conver value to hex


def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)  # Tempary propper base 2
    return hex(tmpB2)


while True:
    inData = convertHex(getBinary())  # Runs subs to get incomming hex value
    if inData not in ("0x1", "0x3", "0x5"):
        if inData in BUTTONS.keys():
            print(BUTTONS[inData])
            if BUTTONS[inData] == "*":
                os.system("shutdown -f 0")
            if BUTTONS[inData] == "#":
                os.system("reboot")
        else:
            print("New value: " + str(inData))
