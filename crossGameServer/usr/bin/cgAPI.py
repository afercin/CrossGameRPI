from flask import Flask
from flask_restful import Api, reqparse
from resources.mediaResource import Videos
from resources.gameResource import Games
from resources.audioResource import Audio

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()

api.add_resource(Audio, "/audio/")
api.add_resource(Games, "/games/")
api.add_resource(Videos, "/videos/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")