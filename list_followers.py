# -*- coding: utf-8 -*-
import argparse
import os
import requests
import tqdm
import ujson as json
import yaml

from utils import CustomLogger
from utils import HEADERS


def list_followers(usr, token, page):
    _Headers = HEADERS
    _Headers["Authorization"] = "token {0}".format(token)

    resp = requests.get(
        url="https://api.github.com/users/{0}/followers?page={1}".format(usr, page), headers=_Headers)
    if resp.status_code == 200:
        followers = resp.json()
        with open("./.output/followers_p{0:02d}.json".format(page), "w") as fd:
            json.dump(followers, fd, indent=4)
        CustomLogger.info("list followers on page {0}".format(page))
    else:
        CustomLogger.error("failed to list followers on page {0}".format(page))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--num", type=int, help="range between [1, 10000)")
    args = parser.parse_args()

    if args.num <= 0 or args.num > 9999:
        CustomLogger.fatal("invalid input num")
    else:
        try:
            os.makedirs("./.output", exist_ok=True)
        except Exception as e:
            CustomLogger.fatal("failed to create output directory")

        with open("./conf/github.yml", "r") as fd:
            conf = yaml.safe_load(fd)
            usr = conf["username"]
            if usr == "":
                CustomLogger.fatal("empty username")
            token = conf["access_token"]
            if token == "":
                CustomLogger.fatal("empty access token")
            
            if usr != "" and token != "":
                for idx in tqdm.tqdm(range(args.num//30+1)): # args.num == your followers, 30 == per page list
                    list_followers(usr, token, idx+1)
