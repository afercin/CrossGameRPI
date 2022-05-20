import os
import configparser
import subprocess

CONFFILE = "/etc/productConf/cg.conf"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameServer" + CONFFILE

config = configparser.ConfigParser()
config.read(CONFFILE)

ROMSPATH = config["PATH"]["roms"]
IMAGEPATH = config["PATH"]["images"]

EMULATORCONTROL = "/tmp/emulator.mode"


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
            games.append(
                {"name": entry, "files": getFilesByPath(f"{folder}/{entry}")})
        else:
            for disk in ls:
                games.append({"name": f"{entry} {disk}", "files": getFilesByPath(
                    f"{folder}/{entry}/{disk}")})
    return games


def getAllGames():
    allGames = []
    for emulator in os.listdir(ROMSPATH):
        if not os.path.isfile(ROMSPATH + "/" + emulator):
            allGames.append(
                {"name": emulator, "games": getGamesByEmulator(emulator)})
    return allGames


def getGameImages(game):
    images = []

    if "Disco" in game:
        game = game.split("Disco")[0].strip()

    if os.path.isfile(f"{IMAGEPATH}/{game}.jpg"):
        images.append(f"{IMAGEPATH}/{game}.jpg")

    if os.path.isfile(f"{IMAGEPATH}/{game}_miniature.jpg"):
        images.append(f"{IMAGEPATH}/{game}_miniature.jpg")

    return images


def openSubprocess(program, args, file, resolution, center=True):
    if resolution:
        window = subprocess.Popen(["/usr/bin/blackWindow.py"])
        os.system(
            f"python3 /usr/bin/changeResolution.py -r {resolution}" + " -c" if center else "")

    subprocess.call(
        [program] + str(args).split(";") + [file])

    if resolution:
        os.system(f"python3 /usr/bin/changeResolution.py -r 1920x1080")
        window.kill()


def launchGame(name, emulator):
    for game in getGamesByEmulator(emulator):
        if name in game["name"]:

            emulatorsPath = config["PATH"]["emulators"]
            emulatorName = config[emulator.upper()]["emulatorName"]
            preferredExtension = config[emulator.upper()]["preferredExtension"]
            resolution = config[emulator.upper()]["resolution"]
            args = config[emulator.upper()]["args"]

            if not preferredExtension:
                isoFile = game["isos"][0]
            else:
                isoFile = next(
                    iso for iso in game["files"] if preferredExtension in iso)

            with open(EMULATORCONTROL, "w") as f:
                f.write(emulatorName)
            
            openSubprocess(program=f"{emulatorsPath}/{emulator}/{emulatorName}",
                           args=args,
                           file=isoFile,
                           resolution=resolution)

            os.remove(EMULATORCONTROL)

            return True

    return False