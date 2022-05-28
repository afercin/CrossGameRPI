#!/usr/bin/env python3
from flask import Flask, request, jsonify
import configparser
from apiResources.audio import *
from apiResources.games import *
from playsound import playsound
import os

CONFFILE = "/etc/productConf/cg.conf"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameUtils" + CONFFILE

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(CONFFILE)

APIPATH = config["PATH"]["api"]

# GAMES
EMULATORCONTROL = config["CONTROL"]["emulator"]


@app.route(f"{APIPATH}/games", methods=["GET"])
def get_games(): return jsonify(getAllGames())


@app.route(f"{APIPATH}/game/images", methods=["GET"])
def get_images_from_game(): return jsonify(getGameImages(request.args["game"]))


@app.route(f"{APIPATH}/game/image", methods=["GET"])
def get_game_image():
    imagePath = request.args["path"]
    if os.path.isfile(imagePath):
        with open(imagePath, "rb") as image:
            f = image.read()
            return bytearray(f)

    return jsonify({"result": "fail"})


@app.route(f"{APIPATH}/game/launch", methods=["GET"])
def launch(): return jsonify({"result": "success" if launchGame(
    request.args["name"], request.args["emulator"]) else "fail"})


@app.route(f"{APIPATH}/game/iconset", methods=["GET"])
def get_iconset(): return jsonify({"result": config["DEFAULT"]["iconset"]})


@app.route(f"{APIPATH}/game/iconset", methods=["POST"])
def set_iconset():
    config["DEFAULT"]["iconset"] = request.args["name"]
    config.write()
    return jsonify({"result": "success"})


# VIDEOS
VIDEOPATH = config["PATH"]["videos"]
VIDEOCONTROL = config["CONTROL"]["video"]


@app.route(f"{APIPATH}/videos", methods=["GET"])
def get_videos(): return jsonify(getFilesByPath(VIDEOPATH))


@app.route(f"{APIPATH}/video/open", methods=["GET"])
def open_video():
    name = request.args["name"]
    videoPath = f"{VIDEOPATH}/{name}"
    """video = cv2.VideoCapture(videoPath)
    height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    print(videoPath)
    print(f"{width}x{height}")

    if width >= 1920 or height >= 1080:
        resolution = ""
    """

    resolution = "720x400"
    with open(VIDEOCONTROL, "w") as f:
        f.write(videoPath)

    openSubprocess(program="vlc",
                   args="-f",
                   file=videoPath,
                   resolution=resolution,
                   center=False)

    os.remove(VIDEOCONTROL)

    return jsonify({"result": "success"})
    return jsonify({"result": "fail"})


# SYSTEM
CROSSGAMEMODE = config["CONTROL"]["crossgame"]
SOUNDSFOLDER = config["PATH"]["sounds"]

def restartx(controlFile):
    if os.path.isfile(controlFile):
        os.remove(controlFile)
        playsound(f"{SOUNDSFOLDER}/enter.wav")
        return os.system("killall crossgameapp") == 0
    return False

@app.route(f"{APIPATH}/system/restartx", methods=["GET"])
def close():
    result = "fail"
    with open(CROSSGAMEMODE) as f:
        mode = f.read()
        if mode == "videos" and restartx(VIDEOCONTROL) or mode == "games" and restartx(EMULATORCONTROL):
            result = "success"
    
    return jsonify({"result": result})


@app.route(f"{APIPATH}/system/audio", methods=["GET"])
def get_audiodevice(): return sinkList()


@app.route(f"{APIPATH}/system/audio", methods=["POST"])
def set_audiodevice(): return jsonify(
    {"result": "success" if setSink(request.args["sink"]) else "fail"})


@app.route(f"{APIPATH}/system/audio/volume-up", methods=["GET"])
def set_volumeUp(): return jsonify(
    {"result": "success" if volumeUp() else "fail"})


@app.route(f"{APIPATH}/system/audio/volume-down", methods=["GET"])
def set_volumeDown(): return jsonify(
    {"result": "success" if volumeDown() else "fail"})


@app.route(f"{APIPATH}/system/audio/toogle", methods=["GET"])
def toogle_audio(): return jsonify(
    {"result": "success" if toogleAudio() else "fail"})


@app.route(f"{APIPATH}/system/mode", methods=["GET"])
def get_crossgame_mode():
    mode = "main"
    if os.path.isfile(CROSSGAMEMODE):
        with open(CROSSGAMEMODE, "r") as f:
            mode = f.read()

    return jsonify({"mode": mode})


@app.route(f"{APIPATH}/system/initialize", methods=["GET"])
def initialize():
    if os.path.isfile(EMULATORCONTROL):
        os.remove(EMULATORCONTROL)

    if os.path.isfile(VIDEOCONTROL):
        os.remove(VIDEOCONTROL)

    setSink(config["DEFAULT"]["sink"])
    setVolume(str(config["DEFAULT"]["volume"]) + "%")
    return jsonify({"result": "success"})

@app.route(f"{APIPATH}/system/bluetooth/devices", methods=["GET"])
def get_bluetooth_devices():
    devices=list()
    for device in subprocess.check_output("bluetoothctl devices", shell=True, text=True).split("\n"):
        if len(device) > 0:
            _, mac, name = device.split(" ", 2)
            devices.append({
                "name": name,
                "mac": mac
            })
    return jsonify(devices)

@app.route(f"{APIPATH}/system/bluetooth/connect", methods=["GET"])
def connect_device():
    device = request.args["device"]
    result = "success"
    if os.system(f"bluetoothctl connect {device}") != 0:
        result = "fail"
    else:
        os.system(f"bluetoothctl trust {device}")
    return jsonify({"result": result})

@app.route(f"{APIPATH}/system/bluetooth/disconnect", methods=["GET"])
def disconnect_device():
    device = request.args["device"]
    result = "success"
    if os.system(f"bluetoothctl disconnect {device}") != 0:
        result = "fail"
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
