from flask import Flask, request, jsonify
from selenium import webdriver
from apiModules.seleniumTv.atresplayerTV import atresplayerTV
from apiModules.seleniumTv.miteleTV import miteleTV
from apiModules.seleniumTv.rtveTV import rtveTV
import configparser
import requests
import json
import os


CHANNELS_FILE = "/etc/productConf/channels.json"
if "dev" in os.path.abspath(os.getcwd()):
    CHANNELS_FILE = "/home/adrix/personal_dev/CrossGameRPI/utils" + CHANNELS_FILE


class tvHandler:
    def __init__(self, config: configparser.ConfigParser):
        self.config = config

        self.updateChannels()
        self.driver = None
        self.currentChannel = 0

    def getDriver(self):
        chrome_options = webdriver.ChromeOptions()
        for option in self.config["TV"]["chromeOptions"].split(";"):
            if option:
                chrome_options.add_argument(option)
        chrome_options.add_experimental_option(
            "excludeSwitches", ['enable-automation'])
        return webdriver.Chrome(chrome_options=chrome_options)

    def updateChannels(self):
        with open(CHANNELS_FILE) as f:
            localList = json.load(f)
        self.channels = localList["channels"]
        try:
            request = requests.get(self.config["TV"]["channelList"]).json()
            if request["updated"] <= localList["updated"]:
                return

            for ambit in request["countries"][0]["ambits"]:
                for ambitChannel in ambit['channels']:
                    for channel in localList["channels"]:
                        if channel["name"] == ambitChannel["name"]:
                            channel["url"] = ambitChannel["web"]
                            channel["logo"] = ambitChannel["logo"]
                            break

            localList["updated"] = request["updated"]
            with open(CHANNELS_FILE, 'w') as f:
                json.dump(localList, f)
        except Exception as e:
            print(e)

    def close(self):
        value = True
        try:
            self.driver.close()
            self.driver = None
            os.remove(self.config['CONTROL']['tv'])
        except:
            value = False
        return value

    def channelDown(self):
        self.currentChannel -= 1
        if self.currentChannel < 1:
            self.currentChannel = len(self.channels)
        return self.setChannel(self.currentChannel)

    def channelUp(self):
        self.currentChannel += 1
        if self.currentChannel > len(self.channels):
            self.currentChannel = 1
        return self.setChannel(self.currentChannel)

    def setChannel(self, number):
        if number > len(self.channels):
            return False

        if self.driver == None:
            os.system(f"touch {self.config['CONTROL']['tv']}")
            self.driver = self.getDriver()
            self.atresplayer = atresplayerTV(self.driver)
            self.mitele = miteleTV(self.driver)
            self.rtve = rtveTV(self.driver)

        self.currentChannel = number
        url = self.channels[number-1]["url"]

        return self.setUrl(url)
    
    def setUrl(self, url):
        if "atresplayer" in url:
            self.atresplayer.setChannel(url)
        elif "mitele" in url:
            self.mitele.setChannel(url)
        elif "rtve" in url:
            self.rtve.setChannel(url)
        else:
            os.system(f"chromium-browser {self.config['TV']['chromeOptions'].replace(';', ' ')} {url}")

        return True


def initializeTvModule(app: Flask, config: configparser.ConfigParser):
    API_PATH = config["PATH"]["api"]

    TV_CONTROL = config["CONTROL"]["tv"]

    tv = tvHandler(config)

    @app.route(f"{API_PATH}/tv/channels", methods=["GET"])
    def get_channels(): return jsonify(tv.channels)

    @app.route(f"{API_PATH}/tv/channel", methods=["GET"])
    def set_channel():
        number = request.args["number"]
        return jsonify({"result": "success" if tv.setChannel(int(number)) else "fail"})

    @app.route(f"{API_PATH}/tv/url", methods=["POST"])
    def set_url():
        url = request.args["url"]
        return jsonify({"result": "success" if tv.setUrl(url) else "fail"})

    @app.route(f"{API_PATH}/tv/channel-down", methods=["GET"])
    def set_channelDown():
        return jsonify({"result": "success" if tv.channelDown() else "fail"})

    @app.route(f"{API_PATH}/tv/channel-up", methods=["GET"])
    def set_channelUp():
        return jsonify({"result": "success" if tv.channelUp() else "fail"})

    @app.route(f"{API_PATH}/tv/power-off", methods=["GET"])
    def tv_powerOff():
        return jsonify({"result": "success" if tv.close() else "fail"})
