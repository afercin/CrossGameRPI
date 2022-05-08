#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import configparser
import os
from apiResources.audio import *
from apiResources.games import *

CONFFILE = "/etc/productConf/cg.conf"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameServer" + CONFFILE

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(CONFFILE)

APIPATH = config["PATH"]["api"]

# GAMES


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

    return jsonify({"message": "fail"})


@app.route(f"{APIPATH}/game/launch", methods=["GET"])
def launch(): return jsonify({"result": "success" if launchGame(
    request.args["name"], request.args["emulator"]) else "fail"})


@app.route(f"{APIPATH}/game/close", methods=["GET"])
def close(): return jsonify({"result": "success" if stopGame() else "fail"})


# VIDEOS
VIDEOPATH = config["PATH"]["videos"]


@app.route(f"{APIPATH}/videos", methods=["GET"])
def get_videos(): return jsonify(getFilesByPath(VIDEOPATH))


@app.route(f"{APIPATH}/video/open", methods=["POST"])
def open_video():
    videoPath = request.args["path"]
    subprocess.call(["vlc", "-f", videoPath])
    return jsonify({"result": "success"})
    return jsonify({"result": "fail"})


# SYSTEM
CROSSGAMEMODE = "/tmp/crossgame.mode"


@app.route(f"{APIPATH}/system/audio", methods=["GET"])
def get_audiodevice(): return sink_list()


@app.route(f"{APIPATH}/system/audio", methods=["POST"])
def set_audiodevice(): return jsonify(
    {"message": "success" if set_sink(request.args["sink"]) else "fail"})


@app.route(f"{APIPATH}/system/audio/volume-up", methods=["GET"])
def set_volumeUp(): return jsonify(
    {"message": "success" if volumeUp() else "fail"})


@app.route(f"{APIPATH}/system/audio/volume-down", methods=["GET"])
def set_volumeDown(): return jsonify(
    {"message": "success" if volumeDown() else "fail"})


@app.route(f"{APIPATH}/system/mode", methods=["GET"])
def get_crossgame_mode():
    mode = "main"
    if os.path.isfile(CROSSGAMEMODE):
        with open(CROSSGAMEMODE, "r") as f:
            mode = f.read()

    return jsonify({"mode": mode})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
