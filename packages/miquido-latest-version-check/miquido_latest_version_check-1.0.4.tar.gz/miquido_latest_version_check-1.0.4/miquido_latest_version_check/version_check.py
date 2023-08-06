import requests
import re
import os
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_latest(repo: str, regex: str = r'[0-9|\.]+'):
    github_token = os.getenv('GITHUB_TOKEN')
    if github_token is None:
        eprint('Missing GITHUB_TOKEN')
        exit(42)

    headers = {'Authorization': f'token {github_token}'}
    res = requests.get(f'https://api.github.com/repos/{repo}/releases/latest', headers=headers)
    # TODO do something with rate limit. Log somewhere
    # print(f'Github rate limit remaining: {res.headers["X-RateLimit-Remaining"]}')
    tag_name = res.json()['tag_name']
    return re.findall(regex, tag_name)[-1]
