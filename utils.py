# -*- coding: utf-8 -*-
import logging
import time

## shared vars

CustomLogger = logging.getLogger("github-openapi-logger")
CustomLogger.setLevel(logging.INFO)
_Handler = logging.StreamHandler()
_Formatter = logging.Formatter("[%(asctime)-15s][%(levelname)-5s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
_Handler.setFormatter(_Formatter)
CustomLogger.addHandler(_Handler)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}

## util functions

def curr_ts():
    return int(time.time())
