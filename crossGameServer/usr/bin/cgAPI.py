#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import os

ROMSPATH = "/rpi/roms"
VIDEOPATH = "/rpi/video"
IMAGEPATH = "/rpi/apptk/images"
APIPATH = "/api/v1"

app = Flask(__name__)

def getFilesByPath(startPath):
    files = []
    for (dirpath, _, filenames) in os.walk(startPath):
        for file in filenames:
            files.append("{}/{}".format(dirpath, file))
    return files

@app.route(f"{APIPATH}/games", methods=["GET"])
def get_games():
    def listFolder(folder):
        data = []
        for entry in os.listdir(folder):

            ls = os.listdir(f"{folder}/{entry}")
            print(ls)
            print(f"{folder}/{entry}/{ls[0]}")

            if os.path.isfile(f"{folder}/{entry}/{ls[0]}"):
                data.append({"name": entry, "files": getFilesByPath(f"{folder}/{entry}")})
            else:
                for disk in ls:
                    data.append({"name": f"{entry} {disk}", "files": getFilesByPath(f"{folder}/{entry}/{disk}")})
        return data

    gameList = []
    for emulator in os.listdir(ROMSPATH):
        if not os.path.isfile(ROMSPATH + "/" + emulator):
            gameList.append({"name": emulator, "games": listFolder(f"{ROMSPATH}/{emulator}")})
    return jsonify(gameList)


@app.route(f"{APIPATH}/videos", methods=["GET"])
def get_videos():
    return jsonify(getFilesByPath(VIDEOPATH))


@app.route(f"{APIPATH}/audio", methods=["GET"])
def get_audiodevice():
    rawText = subprocess.getoutput("pacmd list-sinks")
    audioDevices = {}
    for line in rawText.split("\n"):
        if "index:" in line:
            index = line.split(": ")[1]
            audioDevices[index] = {
                "name": "",
                "active": "*" in line
            }
        if "name:" in line:
            audioDevices[index]["name"] = line.split(": ")[1]

    return audioDevices


@app.route(f"{APIPATH}/audio", methods=["POST"])
def set_audiodevice():
    sink = request.args["sink"]
    if os.system("pacmd set-default-sink {}".format(sink)) == 0:
        return jsonify({'message': 'success'})
    else:
        return jsonify({'message': 'fail'})


@app.route(f"{APIPATH}/images", methods=["GET"])
def get_images_from_game():
    game = request.args["game"]
    images = []

    if "Disco" in game:
        game = game.split("Disco")[0].strip()
        
    if os.path.isfile(f"{IMAGEPATH}/{game}.jpg"):
        images.append(f"{IMAGEPATH}/{game}.jpg")

    if os.path.isfile(f"{IMAGEPATH}/{game}_miniature.jpg"):
        images.append(f"{IMAGEPATH}/{game}_miniature.jpg")

    return jsonify(images)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
