# -*- coding: utf-8 -*-
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
def delete(session, usr, token, repo):
    _Headers = HEADERS
    _Headers["Authorization"] = "token {0}".format(token)

    resp = session.delete(
        url="https://api.github.com/repos/{0}/{1}".format(usr, repo), headers=_Headers)
    if resp.status_code == 204:
        CustomLogger.info("repo <{0}> is deleted".format(repo))
    elif resp.status_code == 403:
        CustomLogger.warning("repo <{0}> is prevented from deletion".format(repo))
    elif resp.status_code == 429:
        raise RateLimitException("api response: 429", 5)  
    else:
        CustomLogger.error("failed to delete repo <{0}>, status code: {1}".format(repo, resp.status_code))


if __name__ == "__main__":
    with open("./conf/github.yml", "r") as fd:
        conf = yaml.safe_load(fd)
        usr = conf["username"]
        if usr == "":
            CustomLogger.fatal("empty username")
        token = conf["access_token"]
        if token == "":
            CustomLogger.fatal("empty access token")
        repos = conf["repos"]
        
        with requests.Session() as session:
            for repo in tqdm.tqdm(repos):
                delete(session, usr, token, repo)
