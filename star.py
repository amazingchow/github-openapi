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
def star(session, owner, token, repo):
    _Headers = HEADERS
    _Headers["Authorization"] = "token {0}".format(token)
    _Headers["Content-Length"] = "0"

    resp = session.put(
        url="https://api.github.com/user/starred/{0}/{1}".format(owner, repo), headers=_Headers)
    if resp.status_code == 204:
        CustomLogger.info("star repo <{0}/{1}>".format(owner, repo))
    elif resp.status_code == 429:
        raise RateLimitException("api response: 429", 5)    
    else:
        CustomLogger.error("failed to star repo <{0}/{1}>, status code: {2}".format(owner, repo, resp.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--owner", type=str, help="owner name")
    parser.add_argument("-r", "--repo", type=str, help="repo name")
    args = parser.parse_args()

    repos = [(args.owner, args.repo)]
    with open("./conf/github.yml", "r") as fd:
        conf = yaml.safe_load(fd)
        usr = conf["username"]
        if usr == "":
            CustomLogger.fatal("empty username")
        token = conf["access_token"]
        if token == "":
            CustomLogger.fatal("empty access token")
        
        with requests.Session() as session:
            for repo in tqdm.tqdm(repos):
                star(session, repo[0], token, repo[1])
