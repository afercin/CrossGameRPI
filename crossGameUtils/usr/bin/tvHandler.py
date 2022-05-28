# /bin/python3

# apt install chromium-chromedriver

from selenium import webdriver
from tv.atresplayerTV import atresplayerTV
from tv.miteleTV import miteleTV
from tv.rtveTV import rtveTV
import configparser
import requests
import json
import os

CONFFILE = "/etc/productConf/cg.conf"
CHANNELS_FILE = "/etc/productConf/channels.json"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/afercin/dev/CrossGameRPI/crossGameUtils" + CONFFILE
    CHANNELS_FILE = "/home/afercin/dev/CrossGameRPI/crossGameUtils" + CHANNELS_FILE


class tvHandler:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read(CONFFILE)

        self.updateChannels()
        self.driver = self.getDriver()

        self.atresplayer = atresplayerTV(self.driver)
        self.mitele = miteleTV(self.driver)
        self.rtve = rtveTV(self.driver)

    def getDriver(self):
        chrome_options = webdriver.ChromeOptions()
        for option in self.config["TV"]["chromeOptions"].split(";"):
            if option:
                chrome_options.add_argument(option)
        chrome_options.add_experimental_option(
            "excludeSwitches", ['enable-automation'])
        return webdriver.Chrome(chrome_options=chrome_options)

    def updateChannels(self):
        request = requests.get(self.config["TV"]["channelList"]).json()
        with open(CHANNELS_FILE) as f:
            localList = json.load(f)
        self.channels = localList["channels"]

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

    def close(self):
        self.driver.close()

    def setChannel(self, number):
        if number > len(self.channels):
            return

        url = self.channels[number-1]["url"]

        if "atresplayer" in url:
            self.atresplayer.setChannel(url)
        elif "mitele" in url:
            self.mitele.setChannel(url)
        elif "rtve" in url:
            self.rtve.setChannel(url)
        else:
            self.driver.get(url)
