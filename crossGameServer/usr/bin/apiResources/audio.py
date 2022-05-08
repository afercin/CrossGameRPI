import subprocess
import os

def sink_list():
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

def set_sink(sinkN):
    return os.system(f"pacmd set-default-sink {sinkN}") == 0

def volumeUp():
    return os.system("amixer -D pulse sset Master 1%+") == 0

def volumeDown():
    return os.system("amixer -D pulse sset Master 1%-") == 0
