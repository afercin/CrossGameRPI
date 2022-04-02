from flask_restful import Resource
import configparser
import os

ROMSPATH = "/rpi/roms"


class Games(Resource):
    def __init__(self):
        CONFFILE = "/etc/productConf/cg.conf"
        if "dev" in os.path.abspath(os.getcwd()):
            CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameServer" + CONFFILE

        self.config = configparser.ConfigParser()
        self.config.read(CONFFILE)

    def getGames(self):
        def listFolder(folder):
            data = {}
            rawList = os.listdir(folder)
            rawList.sort()
            for entry in rawList:
                if os.path.isfile(folder + "/" + entry):
                    return rawList
                else:
                    data[entry] = listFolder(folder + "/" + entry)
            return data

        gameList = {}
        for emulator in os.listdir(ROMSPATH):
            if not os.path.isfile(ROMSPATH + "/" + emulator):
                gameList[emulator] = listFolder(ROMSPATH + "/" + emulator)
        return gameList

    def get(self):
        return self.getGames(), 201

    def post(self, emulator, game, disk):
        gameList = self.getGames()
        if game in gameList[emulator]:

            path = "{}/{}/{}".format(ROMSPATH, emulator, game)
            if disk is not None:
                path += "/" + disk

            for file in os.listdir(path):
                if self.config[emulator]["preferredExtension"] in file:
                    path += "/" + file

            os.system("/usr/share/server/emulators/{} {} {}".format(
                emulator,
                self.config[emulator]["args"],
                file))
        else:
            return "Game not found", 404
