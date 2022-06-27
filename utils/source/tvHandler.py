# /bin/python3

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
        value = True
        try:
            self.driver.close()
            self.driver =  None
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

        if "atresplayer" in url:
            self.atresplayer.setChannel(url)
        elif "mitele" in url:
            self.mitele.setChannel(url)
        elif "rtve" in url:
            self.rtve.setChannel(url)
        else:
            self.driver.get(url)
            
        return True
