#!/usr/bin/env python3
from apiModules.system import initializeSystemModule
from apiModules.media import initializeMediaModule
from apiModules.tv import initializeTvModule
from flask import Flask
import configparser
import os

CONFFILE = "/etc/productConf/cg.conf"
if "dev" in os.path.abspath(os.getcwd()):
    CONFFILE = "/home/adrix/personal_dev/CrossGameRPI/utils" + CONFFILE

app = Flask(__name__)

config = configparser.ConfigParser()
config.read(CONFFILE)

initializeSystemModule(app, config)
initializeMediaModule(app, config)
initializeTvModule(app, config)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
