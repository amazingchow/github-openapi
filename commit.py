# -*- coding: utf-8 -*-
import argparse
import base64
import requests
import yaml

from utils import curr_ts
from utils import CustomLogger
from utils import HEADERS


def commit(usr, email, token, repo):
    _Headers = HEADERS
    _Headers["Authorization"] = "token {0}".format(token)

    content = "hello world"
    encoded_content = str(base64.b64encode(content.encode("utf-8")), "utf-8")
    payload = {
        "message": "my commit message",
        "committer": {
            "name": usr,
            "email": email
        },
        "content": encoded_content
    }

    resp = requests.put(
        url="https://api.github.com/repos/{0}/{1}/contents/hello_{2}.txt".format(usr, repo, curr_ts()), 
        headers=HEADERS, json=payload)
    if resp.status_code == 201:
        CustomLogger.info("repo {0} has one new commit".format(repo))
    else:
        CustomLogger.error("failed to create one commit for repo {0}, status code: {1}".format(repo, resp.status_code))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--repo", type=str, help="repo name")
    args = parser.parse_args()

    repo = args.repo
    with open("./conf/github.yml", "r") as fd:
        conf = yaml.safe_load(fd)
        usr = conf["username"]
        if usr == "":
            CustomLogger.fatal("empty username")
        token = conf["access_token"]
        if token == "":
            CustomLogger.fatal("empty access token")
        email = conf["email"]
        if email == "":
            CustomLogger.fatal("empty email")
        
        if usr != "" and token != "" and email != "":
            commit(usr, email, token, repo)
