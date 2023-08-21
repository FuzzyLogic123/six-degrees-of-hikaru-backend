from httplib2 import FailedToDecompressContent
import requests
import time
import json
from rich.progress import track
import jsonlines
from rich.console import Console

import queue, time, urllib.request
from threading import Thread

with open('./data/root.json', 'r') as file:
    root = json.load(file)
TIME_CONTROL = "bullet"
URL_LOCATION = './data/request_urls/requests.txt'

def get_request_urls(player_list, time_class, path_to_save_file):
    failed_requests = []
    lambda_archive_request_urls = ""
    with open(path_to_save_file, "w") as file:
        file.write("username,time_class,archive_url\n")

        for player_username in track(player_list):
            lambda_archive_request_urls = ""
            print(player_username)
            url = f"https://api.chess.com/pub/player/{player_username}/games/archives"

            try:
                request = requests.get(url)
                response_json = request.json()
                archives = response_json["archives"]
            except:
                failed_requests.append(url)
            for archive in archives:
                lambda_archive_request_urls += f"{player_username},{time_class},{archive}\n"
            file.write(lambda_archive_request_urls)
    print("finished getting archive urls...")
    return failed_requests

failed_requests = get_request_urls(root, TIME_CONTROL, URL_LOCATION)
with open('./data/request_urls/failures.txt', 'w'):
    for request in failed_requests:
        file.write(request + "\n")