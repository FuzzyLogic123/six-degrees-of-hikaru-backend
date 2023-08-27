import json
import queue
import time
import urllib.request
from threading import Thread
from config import TIME_CONTROL, DEGREE, URL_LOCATION
import requests
from rich.console import Console
from rich.progress import track

from utils import get_root_players

root = get_root_players(DEGREE, TIME_CONTROL)

def get_request_urls(player_list, path_to_save_file):
    failed_requests = []
    lambda_archive_request_urls = ""
    with open(path_to_save_file, "w") as file:
        file.write("username|time_class|archive_url\n")
        for player_username in track(player_list):
            lambda_archive_request_urls = ""
            print(player_username)
            url = f"https://nlfezg5oid35cygimbmnxcsnee0ehmgk.lambda-url.us-west-1.on.aws/?url=https://api.chess.com/pub/player/{player_username}/games/archives"

            try:
                request = requests.get(url)
                response_json = request.json()
                archives = response_json
            except:
                failed_requests.append(url)
                
            for archive in archives:
                lambda_archive_request_urls += f"{player_username}|{TIME_CONTROL}|{archive}\n"
            file.write(lambda_archive_request_urls)
    print("finished getting archive urls...")
    return failed_requests

failed_requests = get_request_urls(root, f'{URL_LOCATION}/requests.txt')

with open(f'{URL_LOCATION}/url_fetch_failures.txt', 'a') as file:
    file.write("\n")
    for request in failed_requests:
        file.write(request + "\n")