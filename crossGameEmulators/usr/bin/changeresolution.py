#!/usr/bin/python
import sys
import getopt
import subprocess
import os
from screeninfo import get_monitors


def main(argv):
    rflag = False
    aflag = False
    nflag = False
    try:
        opts, args = getopt.getopt(argv, "hncr:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("changeResolution.py -r <resolution> [-c] [-n]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("changeResolution.py -r <resolution> [-c] [-n]")
            sys.exit()
        elif opt == "-r":
            rflag = True
            resolution = arg
        elif opt == "-c":
            cflag = True
        elif opt == "-n":
            nflag = True

    if rflag:
        x, y = resolution.split("x")
        output = get_monitors()[0].name

        if nflag:
            config = subprocess.check_output(
                "cvt {} {} 60".format(x, y), shell=True, text=True).split("\n")[1].split(' ', 1)[1].replace("\"", "")
            mode = config.split(" ")[0]
            os.system("xrandr --newmode {}".format(config))
            os.system("xrandr --addmode {} {}".format(output, mode))
        else:
            mode = resolution

        options = "--output {} --mode {}".format(output, mode)

        if cflag:
            aspectRatio = round(float(x) / float(y), 8)
            xoffset = (int(x) * float(aspectRatio) - int(x)) / 2
            options += " --panning {} --transform {},0,-{},0,1,0,0,0,1".format(
                mode, aspectRatio, xoffset)

        os.system("xrandr {}".format(options))


if __name__ == "__main__":
    main(sys.argv[1:])
