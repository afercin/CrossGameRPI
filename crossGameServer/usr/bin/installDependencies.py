import os
from logUtils import *
import subprocess


class installDependencies:
    DEPENDENCIES = ("imutils", "opencv-python", "python-vlc",
                    "ds4drv", "screeninfo", "pygame", "rpi.gpio", "pynput")

    def __init__(self):
        if os.path.isfile("/etc/productConf/product.version"):
            with open("/etc/productConf/product.version", "r") as f:
                self.version = f.readline()
        else:
            with open("/etc/productConf/product.version", "w") as f:
                f.write("0.0")
            self.version = 0.0
        self.log = logUtils()

    def install(self):
        self.log.info("Comprobando si hay dependencias por instalar...")

        version = subprocess.getoutput(
            "dpkg -l | grep crossgameapp | awk '{print $3}' | head -1").replace("'", "")
        if version > self.version:
            self.log.info(
                "Detectado cambio de versión, comprobando las dependencias...")

            os.system("pip install --upgrade pip > /dev/null 2>&1")

            for d in self.DEPENDENCIES:
                os.system("pip install -- user {} > /dev/null 2>&1".format(d))

            with open("/etc/productConf/product.version", "w") as f:
                f.write(version)

            self.log.info("Dependencias instaladas correctamente")

        else:
            self.log.info("No hay dependencias por instalar")

        with open("/tmp/crossgame.ready", "w") as f:
            f.write("ready")

    def dispose(self):
        self.log.dispose()


if (__name__ == "__main__"):
    i = installDependencies()
    i.install()
    i.dispose()
