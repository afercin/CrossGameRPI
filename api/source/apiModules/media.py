from flask import Flask, request, jsonify
import configparser
import subprocess
import os

DEFAULT_RESOLUTION = "1920x1080"


def getFilesByPath(startPath):
    files = []
    for (dirpath, _, filenames) in os.walk(startPath):
        for file in filenames:
            files.append("{}/{}".format(dirpath, file))
    return files


def openSubprocess(program, args, file, resolution, center=True):
    if resolution:
        os.system(
            f"changeResolution -r {resolution}" + (" -c" if center else ""))

    subprocess.call(
        [program] + str(args).split(";") + [file])

    if resolution:
        os.system(f"changeResolution -r {DEFAULT_RESOLUTION}")


def initializeMediaModule(app: Flask, config: configparser.ConfigParser):
    API_PATH = config["PATH"]["api"]
    ROMS_PATH = config["PATH"]["roms"]
    IMAGES_PATH = config["PATH"]["images"]
    VIDEOS_PATH = config["PATH"]["videos"]

    EMULATOR_CONTROL_FILE = config["CONTROL"]["emulator"]
    DEFAULT_RESOLUTION = config["DEFAULT"]["resolution"]

    # Images
    @app.route(f"{API_PATH}/game/images", methods=["GET"])
    def get_images_from_game():
        game = request.args["game"]
        images = []

        if "Disco" in game:
            game = game.split("Disco")[0].strip()

        if os.path.isfile(f"{IMAGES_PATH}/{game}.jpg"):
            images.append(f"{IMAGES_PATH}/{game}.jpg")

        if os.path.isfile(f"{IMAGES_PATH}/{game}_miniature.jpg"):
            images.append(f"{IMAGES_PATH}/{game}_miniature.jpg")

        return jsonify(images)

    @app.route(f"{API_PATH}/game/image", methods=["GET"])
    def get_game_image():
        imagePath = request.args["path"]
        if os.path.isfile(imagePath):
            with open(imagePath, "rb") as image:
                f = image.read()
                return bytearray(f)

        return jsonify({"result": "fail"})

    # Games
    def getGamesByEmulator(emulator):
        folder = f"{ROMS_PATH}/{emulator}"
        games = []
        for entry in os.listdir(folder):

            ls = os.listdir(f"{folder}/{entry}")

            if os.path.isfile(f"{folder}/{entry}/{ls[0]}"):
                games.append(
                    {"name": entry, "files": getFilesByPath(f"{folder}/{entry}")})
            else:
                for disk in ls:
                    games.append({"name": f"{entry} {disk}", "files": getFilesByPath(
                        f"{folder}/{entry}/{disk}")})
        return games

    def getAllGames():
        allGames = []
        for emulator in os.listdir(ROMS_PATH):
            if not os.path.isfile(ROMS_PATH + "/" + emulator):
                allGames.append(
                    {"name": emulator, "games": getGamesByEmulator(emulator)})
        return allGames

    @app.route(f"{API_PATH}/games", methods=["GET"])
    def get_games(): return jsonify(getAllGames())

    @app.route(f"{API_PATH}/game/launch", methods=["GET"])
    def launch():
        name = request.args["name"]
        emulator = request.args["emulator"]
        if name == "Steam":
            os.system("touch /tmp/steam.mode && restartx")
        for game in getGamesByEmulator(emulator):
            if name in game["name"]:

                emulatorName = config[emulator.upper()]["emulatorName"]
                preferredExtension = config[emulator.upper(
                )]["preferredExtension"]
                resolution = config[emulator.upper()]["resolution"]
                args = config[emulator.upper()]["args"]

                if not preferredExtension:
                    isoFile = game["files"][0]
                else:
                    isoFile = next(
                        iso for iso in game["files"] if preferredExtension in iso)

                with open(EMULATOR_CONTROL_FILE, "w") as f:
                    f.write(emulatorName)

                openSubprocess(program=emulatorName,
                               args=args,
                               file=isoFile,
                               resolution=resolution)

                os.remove(EMULATOR_CONTROL_FILE)

                return jsonify({"result": "success"})

        return jsonify({"result": "fail"})

    @app.route(f"{API_PATH}/game/iconset", methods=["GET"])
    def get_iconset(): return jsonify({"result": config["DEFAULT"]["iconset"]})

    @app.route(f"{API_PATH}/game/iconset", methods=["POST"])
    def set_iconset():
        config["DEFAULT"]["iconset"] = request.args["name"]
        config.write()
        return jsonify({"result": "success"})

    # Videos

    @app.route(f"{API_PATH}/videos", methods=["GET"])
    def get_videos():
        videos = getFilesByPath(VIDEOS_PATH)
        for i in range(8):
            if os.path.exists(f"/media/usb{i}/video"):
                videos += getFilesByPath(f"/media/usb{i}/video")
            if os.path.exists(f"/media/usb{i}/Videos"):
                videos += getFilesByPath(f"/media/usb{i}/Videos")
        return jsonify(videos)
