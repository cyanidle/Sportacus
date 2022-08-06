# -*- coding: utf-8 -*-
from src.sportacus import Sportacus
from python_redis_lib.settings import Reader
from python_redis_lib.initlogging import initLogging

def main():
    logging_conf_reader = Reader(file="logging.toml")
    initLogging(__file__, settings=logging_conf_reader.parseLogging())
    sportacus = Sportacus()
    sportacus.init()
    sportacus.run()

if __name__ == "__main__":
    main()
