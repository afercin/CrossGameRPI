from datetime import datetime
import configparser
import logging
import inspect
import os


class logger():
    def __init__(self, config:configparser.ConfigParser, verbose=False):
        if not config.has_section("LOG"):
            print("ERROR - Config file has not section LOG.")
            os._exit(3)

        self.script_name = os.path.basename(
            inspect.stack()[-1].filename).split(".")[0]
        self.verbose = verbose

        # Definicion logger
        logger_name = f"{self.script_name}-logger"
        log_folder = config["LOG"]["log_folder"]
        log_file = self.script_name
        log_level = config["LOG"]["log_level"]
        log_format = f"[ {self.script_name} ]" + '[%(asctime)s] [%(levelname)s] %(message)s'

        self.log_path = log_folder + log_file + ".log"

        try:
            self.logger = logging.getLogger(logger_name)
            self.file_logger = logging.FileHandler(self.log_path)
            self.file_formatter = logging.Formatter(log_format)
            self.file_logger.setFormatter(self.file_formatter)
            self.logger.addHandler(self.file_logger)
            self.logger.setLevel(log_level)
        except Exception as error:
            print("Error with logs: %s") % (str(error))
            os._exit(4)

        self.printHead()

    def printHead(self) -> None:
        with open(self.log_path, "a") as f:
            f.write("◤━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◥\n")

    def printTail(self):
        with open(self.log_path, "a") as f:
            f.write("◣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━◢\n")
            f.write("\n")

    def info(self, msg: str) -> None:
        self.printMsg(msg, "INFO")

    def warn(self, msg: str) -> None:
        self.printMsg(msg, "WARN")

    def error(self, msg: str, exit_code=-1) -> None:
        self.printMsg(msg, "ERROR")
        if exit_code != -1:
            self.printTail()
            os._exit(exit_code)

    def printMsg(self, msg: str, level) -> None:
        if self.verbose:
            date = str(datetime.now())
            print(f"[ {self.script_name} ][{date}][{level}] {msg}")

        if level == "INFO":
            self.logger.info(msg)

        if level == "WARN":
            self.logger.warning(msg)

        if level == "ERROR":
            self.logger.error(msg)
            

def start_logger(config: configparser.ConfigParser, verbose=False) -> logger:
    return logger(config, verbose)