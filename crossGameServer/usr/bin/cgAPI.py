#!/usr/bin/env python3
from flask import Flask, request, jsonify
import subprocess
import configparser
import os

CONFFILE = "/etc/productConf/cg.conf"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameServer" + CONFFILE

config = configparser.ConfigParser()
config.read(CONFFILE)

ROMSPATH = config["PATH"]["roms"]
VIDEOPATH = config["PATH"]["videos"]
IMAGEPATH = config["PATH"]["images"]
APIPATH = config["PATH"]["api"]

EMULATORCONTROL = "/tmp/emulator.mode"

app = Flask(__name__)

def getFilesByPath(startPath):
    files = []
    for (dirpath, _, filenames) in os.walk(startPath):
        for file in filenames:
            files.append("{}/{}".format(dirpath, file))
    return files

def getGamesByEmulator(emulator):
    folder = f"{ROMSPATH}/{emulator}"
    games = []
    for entry in os.listdir(folder):

        ls = os.listdir(f"{folder}/{entry}")

        if os.path.isfile(f"{folder}/{entry}/{ls[0]}"):
            games.append({"name": entry, "files": getFilesByPath(f"{folder}/{entry}")})
        else:
            for disk in ls:
                games.append({"name": f"{entry} {disk}", "files": getFilesByPath(f"{folder}/{entry}/{disk}")})
    return games

def getAllGames():
    allGames = []
    for emulator in os.listdir(ROMSPATH):
        if not os.path.isfile(ROMSPATH + "/" + emulator):
            allGames.append({"name": emulator, "games": getGamesByEmulator(emulator)})
    return allGames

@app.route(f"{APIPATH}/games", methods=["GET"])
def get_games():
    return jsonify(getAllGames())


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

@app.route(f"{APIPATH}/get-miniature", methods=["GET"]) 
def get_game_miniature():
    game = request.args["game"]
    image = None

    if "Disco" in game:
        game = game.split("Disco")[0].strip()

    if os.path.isfile(f"{IMAGEPATH}/{game}_miniature.jpg"):
        with open(f"{IMAGEPATH}/{game}_miniature.jpg", "rb") as image:
            f = image.read()
            return bytearray(f)

    return jsonify({'message': 'fail'})

@app.route(f"{APIPATH}/launch-game", methods=["GET"]) 
def launch_game():
    name = request.args["name"]
    emulator = request.args["emulator"]

    for game in getGamesByEmulator(emulator):
        if name in game["name"]:

            emulatorsPath = config["PATH"]["emulators"]
            emulatorName = config[emulator.upper()]["emulatorName"]
            preferredExtension = config[emulator.upper()]["preferredExtension"]
            resolution = config[emulator.upper()]["resolution"]
            args = config[emulator.upper()]["args"]

            if not preferredExtension:
                isoFile = game["isos"][0];
            else:
                isoFile = next(iso for iso in game["files"] if preferredExtension in iso)

            if resolution:
                window = subprocess.Popen(["/usr/bin/blackWindow.py"])
                os.system(f"python3 /usr/bin/changeResolution.py -r {resolution} -c")
            
            with open(EMULATORCONTROL, "w") as f:
                f.write(emulatorName)

            subprocess.call([f"{emulatorsPath}/{emulator}/{emulatorName}"] + str(args).split(";") +[isoFile])

            os.remove(EMULATORCONTROL)

            if resolution:
                os.system(f"python3 /usr/bin/changeResolution.py -r 1920x1080")
                window.kill()
            
            return jsonify({'result': "Ok"})

    return jsonify({'result': "Not ok"})

@app.route(f"{APIPATH}/close-emulator", methods=["GET"]) 
def close_emulator():
    if os.path.isfile(EMULATORCONTROL):
        os.remove(EMULATORCONTROL)
        os.system("killall crossgame")
        return jsonify({'result': "Ok"})

    return jsonify({'result': "Not ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
