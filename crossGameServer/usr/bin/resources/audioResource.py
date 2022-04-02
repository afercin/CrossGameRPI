from flask_restful import Resource
import subprocess
import os


class Audio(Resource):
    def getAudioDevices(self):
        rawText = subprocess.getoutput("pacmd list-sinks")
        self.audioDevices = {}
        for line in rawText.split("\n"):
            if "index:" in line:
                index = line.split(": ")[1]
                self.audioDevices[index] = {
                    "name": "",
                    "active": "*" in line
                }

            if "name:" in line:
                self.audioDevices[index]["name"] = line.split(": ")[1]

    def get(self):
        self.getAudioDevices()
        return self.audioDevices, 201

    def post(self, sink):
        self.getAudioDevices()
        if sink in self.audioDevices:
            return os.system("pacmd set-default-sink {}".format(sink)), 201
        else:
            return "Sink number not found", 404
