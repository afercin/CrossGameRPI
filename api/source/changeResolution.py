#!/usr/bin/env python3
import sys
import getopt
import subprocess
import os
import requests
import json


def main(argv):
    rflag = False
    cflag = False
    nflag = False
    try:
        opts, args = getopt.getopt(argv, "hncr:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print("changeResolution -r <resolution> [-c] [-n]")
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print("changeResolution -r <resolution> [-c] [-n]")
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
        output = json.loads(requests.get("http://localhost:5000/api/v1/system/screens").text)[0]["display"]

        if nflag:
            config = subprocess.check_output(
                f"cvt {x} {y} 60", shell=True, text=True).split("\n")[1].split(' ', 1)[1].replace("\"", "")
            mode = config.split(" ")[0]
            os.system(f"xrandr --newmode {config}")
            os.system(f"xrandr --addmode {output} {mode}")
        else:
            mode = resolution

        options = f"--output {output} --mode {mode} --panning {mode}"

        if cflag:
            aspectRatio = round(float(x) / float(y), 8)
            xoffset = (int(x) * float(aspectRatio) - int(x)) / 2
            options += f" --transform {aspectRatio},0,-{xoffset},0,1,0,0,0,1"
        else:
            options += f" --transform 1,0,0,0,1,0,0,0,1"
        
        os.system(f"xrandr {options}")


if __name__ == "__main__":
    main(sys.argv[1:])
