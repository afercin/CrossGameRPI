#!/usr/bin/python
import sys
import getopt
import os
import time


def _find_getch():
    try:
        import termios
    except ImportError:
        # Non-POSIX. Return msvcrt's (Windows') getch.
        import msvcrt
        return msvcrt.getch

    # POSIX system. Create and return a getch that manipulates the tty.
    import sys
    import tty

    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

    return _getch


def main(argv):
    sflag = False
    cflag = False
    file = "/tmp/keys"
    try:
        opts, args = getopt.getopt(argv, "hsc")
    except getopt.GetoptError:
        print("simulateKeys.py -c")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("simulateKeys.py -c")
            sys.exit()
        elif opt == "-c":
            cflag = True
            resolution = arg
        elif opt == "-s":
            sflag = True

    if sflag:
        from pynput.keyboard import Controller, Key
        os.system("echo '' > " + file)
        tiempo = os.path.getmtime(file)
        keyboard = Controller()
        SPECIALKEYS = {
            "OP": Key.f1,
            "OQ": Key.f2,
            "OR": Key.f3,
            "OS": Key.f4,
            "[15~": Key.f5,
            "[17~": Key.f6,
            "[18~": Key.f7,
            "[19~": Key.f8,
            "[20~": Key.f9,
            "[21~": Key.f10,
            "[24~": Key.f12,
            "[A": Key.up,
            "[B": Key.down,
            "[D": Key.left,
            "[C": Key.right,
            "127": Key.backspace,
            "13": Key.enter,
            "tab": Key.tab
        }
        while True:
            if tiempo != os.path.getmtime(file) and not os.path.isfile("/tmp/keylock"):
                os.system("echo '' > /tmp/keylock")
                with open(file, "r") as f:
                    key = f.read()
                    if len(key) > 1:
                        key = SPECIALKEYS[key]
                    os.system(
                        "echo 'Simulating: {}' >> /tmp/pruebakeys".format(key))
                    keyboard.press(key)
                    keyboard.release(key)
                os.system("rm /tmp/keylock")
                tiempo = os.path.getmtime(file)
            time.sleep(0.025)

    if cflag:
        print("Capturing input... Press CTRL + C to exit")
        os.system("rm /tmp/keylock")
        getch = _find_getch()
        key = "a"
        while ord(key) != 3:
            key = getch()
            while os.path.isfile("/tmp/keylock"):
                time.sleep(0.025)
            if ord(key) == 27:
                specialKey = getch()
                k = getch()
                if ord(k) < 65:
                    k += getch() + getch()
                specialKey += k
                key = specialKey
            elif ord(key) == 127 or ord(key) == 13:
                key = str(ord(key))
            elif ord(key) == 9:
                key = "tab"
            if len(key) > 1 or ord(key) != 3:  # ctrl + c
                os.system("echo '' > /tmp/keylock")
                with open(file, "w") as f:
                    f.write(str(key))
                os.system("rm /tmp/keylock")
            if len(key) > 1:
                key = "a"


if __name__ == "__main__":
    main(sys.argv[1:])
