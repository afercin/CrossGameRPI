from flask import Flask, request, jsonify
from pydub.playback import play
from pydub import AudioSegment
import configparser
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


def setSink(sinkN) -> bool:
    return os.system(f"pacmd set-default-sink {sinkN}") == 0


def setVolume(volume, checkHdmi=False) -> bool:
    sinks = sinkList()
    if checkHdmi:
        for i in range(0, len(sinks)):
            if "alsa_output.platform-fef05700.hdmi.iec958-stereo" in sinks[f"{i}"]["name"] and sinks[f"{i}"]["active"]:
                return False
    return os.system(f"amixer -D pulse set Master {volume}") == 0


def initializeSystemModule(app: Flask, config: configparser.ConfigParser):
    API_PATH = config["PATH"]["api"]
    CROSSGAME_MODE_FILE = config["PATH"]["mode"]
    SOUND_FOLDER = config["PATH"]["sounds"]

    TV_CONTROL_FILE = config["CONTROL"]["tv"]
    EMULATOR_CONTROL_FILE = config["CONTROL"]["emulator"]

    QUIT_SOUND = AudioSegment.from_wav(f"{SOUND_FOLDER}/enter.wav")

    # Audio
    @app.route(f"{API_PATH}/system/audio", methods=["GET"])
    def get_audiodevice(): return sinkList()

    @app.route(f"{API_PATH}/system/audio", methods=["POST"])
    def set_audiodevice(): return jsonify(
        {"result": "success" if setSink(request.args["sink"]) else "fail"})

    @app.route(f"{API_PATH}/system/audio/volume-up", methods=["GET"])
    def set_volumeUp(): return jsonify(
        {"result": "success" if setVolume("5%+", True) else "fail"})

    @app.route(f"{API_PATH}/system/audio/volume-down", methods=["GET"])
    def set_volumeDown(): return jsonify(
        {"result": "success" if setVolume("5%-", True) else "fail"})

    @app.route(f"{API_PATH}/system/audio/toogle", methods=["GET"])
    def toogle_audio(): return jsonify(
        {"result": "success" if setVolume("toggle", True) else "fail"})

    # Utils
    @app.route(f"{API_PATH}/system/restartx", methods=["GET"])
    def close():
        play(QUIT_SOUND)
        return os.system("killall crossgameapp") == 0
        def restartx(controlFile):
            if os.path.isfile(controlFile):
                os.remove(controlFile)
                play(QUIT_SOUND)
                return os.system("killall crossgameapp") == 0
            return False

        result = "fail"
        with open(CROSSGAME_MODE_FILE) as f:
            mode = f.read()
            if mode == "games" and restartx(EMULATOR_CONTROL_FILE) or \
               mode == "tv" and restartx(TV_CONTROL_FILE):
                result = "success"

        return jsonify({"result": result})

    @app.route(f"{API_PATH}/system/mode", methods=["GET"])
    def get_crossgame_mode():
        mode = "main"
        if os.path.isfile(CROSSGAME_MODE_FILE):
            with open(CROSSGAME_MODE_FILE, "r") as f:
                mode = f.read()

        return jsonify({"mode": mode})

    @app.route(f"{API_PATH}/system/initialize", methods=["GET"])
    def initialize():
        for controlFile in config["CONTROL"]:
            if os.path.isfile(controlFile):
                os.remove(controlFile)

        setSink(config["DEFAULT"]["sink"])
        setVolume(str(config["DEFAULT"]["volume"]) + "%")
        return jsonify({"result": "success"})

    # Bluetooth
    @app.route(f"{API_PATH}/system/bluetooth/devices", methods=["GET"])
    def get_bluetooth_devices():
        devices = list()
        for device in subprocess.check_output("bluetoothctl devices", shell=True, text=True).split("\n"):
            if len(device) > 0:
                _, mac, name = device.split(" ", 2)
                devices.append({
                    "name": name,
                    "mac": mac
                })
        return jsonify(devices)

    @app.route(f"{API_PATH}/system/bluetooth/connect", methods=["GET"])
    def connect_device():
        device = request.args["device"]
        result = "success"
        if os.system(f"bluetoothctl connect {device}") != 0:
            result = "fail"
        else:
            os.system(f"bluetoothctl trust {device}")
        return jsonify({"result": result})

    @app.route(f"{API_PATH}/system/bluetooth/disconnect", methods=["GET"])
    def disconnect_device():
        device = request.args["device"]
        result = "success"
        if os.system(f"bluetoothctl disconnect {device}") != 0:
            result = "fail"
        return jsonify({"result": result})
