import subprocess
import os


def sinkList():
    rawText = subprocess.getoutput("pacmd list-sinks")
    sinks = {}
    for line in rawText.split("\n"):
        if "index:" in line:
            index = line.split(": ")[1]
            sinks[index] = {
                "name": "",
                "active": "*" in line
            }
        if "name:" in line:
            sinks[index]["name"] = line.split(": ")[1]

    return sinks


def setSink(sinkN): return os.system(f"pacmd set-default-sink {sinkN}") == 0


def volumeUp(): return setVolume("5%+")


def volumeDown(): return setVolume("5%-")


def toogleAudio(): return setVolume("toggle")


def setVolume(volume):
    sinks = sinkList()
    for i in range(0, len(sinks)):
        if "alsa_output.platform-fef05700.hdmi.iec958-stereo" in sinks[f"{i}"]["name"] and sinks[f"{i}"]["active"]:
            return False;
    return os.system(f"amixer -D pulse set Master {volume}") == 0
