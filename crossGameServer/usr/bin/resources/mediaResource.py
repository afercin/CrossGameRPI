from flask_restful import Resource
import os

VIDEOPATH = "/rpi/video"


class Videos(Resource):
    def get(self):
        f = []
        for (dirpath, _, filenames) in os.walk(VIDEOPATH):
            for file in filenames:
                f.append("{}/{}".format(dirpath, file))

        return f, 201
