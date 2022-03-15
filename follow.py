# -*- coding: utf-8 -*-
import argparse
import requests
import tqdm
import yaml

from ratelimit import limits
from ratelimit import RateLimitException
from ratelimit import sleep_and_retry
from utils import CustomLogger
from utils import HEADERS


@sleep_and_retry
@limits(calls=5000, period=3600)
def follow(session, _, token, following):
    _Headers = HEADERS
    _Headers["Authorization"] = "token {0}".format(token)
    _Headers["Content-Length"] = "0"

    resp = session.put(
        url="https://api.github.com/user/following/{0}".format(following), headers=_Headers)
    if resp.status_code == 204:
        CustomLogger.info("follow people <{0}>".format(following))
    elif resp.status_code == 429:
        raise RateLimitException("api response: 429", 5)
    else:
        CustomLogger.error("failed to follow people <{0}>, status code: {1}".format(following, resp.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, help="github id")
    args = parser.parse_args()

    followings = [args.username]
    with open("./conf/github.yml", "r") as fd:
        conf = yaml.safe_load(fd)
        usr = conf["username"]
        if usr == "":
            CustomLogger.fatal("empty username")
        token = conf["access_token"]
        if token == "":
            CustomLogger.fatal("empty access token")
        
        with requests.Session() as session:
            for following in tqdm.tqdm(followings):
                follow(session, usr, token, following)
