import json
import queue
import time
import urllib.request
from fileinput import filename
from threading import Thread
import json
import requests
from rich import print
from rich.console import Console
from rich.progress import track

from config import DEGREE, IS_FAILURES, TIME_CONTROL, URL_LOCATION, MAX_CONCURRENT_REQUESTS

from utils import get_usernames_found_set

player_losses = {}

def get_player_losses():
    path_to_request_list = URL_LOCATION
    with open(path_to_request_list + ("/failures.txt" if IS_FAILURES else "/requests.txt"), 'r+') as file:
        urls = []
        for line in file:
            if IS_FAILURES:
                urls += [line.strip()]
            else:
                username, time_class, archive_url = line.strip().split("|")
                if (time_class != "time_class"):
                    urls += [f"https://iaprgyb7j4t7ymppwyzewul5ei0wfrqp.lambda-url.us-west-1.on.aws/?time_class={time_class}&url={archive_url}&username={username}"]

    players_completed = get_usernames_found_set()
    perform_web_requests(urls, MAX_CONCURRENT_REQUESTS, players_completed)
    return player_losses

#class for doing multiple requests at once
def perform_web_requests(addresses, no_workers, players_completed):
    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.results = []

        def run(self):
            while True:
                try:
                    content = self.queue.get(False)
                except queue.Empty as e:
                    break
                # if content == "":
                #     break
                try:
                    request = urllib.request.Request(content)
                    response = urllib.request.urlopen(request)

                    if response.getcode() != 200:
                        raise Exception(f"Error fetching chess.com archive: {response.getcode()}")

                    #process data
                    result = json.loads(response.read())
                    current_player = result["player"]
                    if not player_losses.get(current_player):
                        player_losses[current_player] = {
                            "losses": set(),
                        }
                    player_losses[current_player]["losses"].update(x for x in result["player_losses"] if x not in players_completed)
                    players_completed.update(result["player_losses"]) # update the set of completed players
                    self.results.append(response.read())
                    self.queue.task_done()
                    print(f"[green]{current_player}")
                except Exception as e:
                    print(f"[red]{e.read().decode('utf-8')}")
                    print(f"[red]{content}")
                    with open(f'{URL_LOCATION}/failures.txt', 'a') as file:
                        file.write(content + "\n")

    # Create queue and add addresses
    q = queue.Queue()
    for url in addresses:
        q.put(url)

    # Workers keep working till they receive an empty string
    # for _ in range(no_workers):
    #     q.put("")

    # Create workers and add tot the queue
    workers = []
    for _ in range(no_workers):
        worker = Worker(q)
        worker.start()
        workers.append(worker)
    # Join workers to wait till they finished
    for worker in workers:
        worker.join()

    # Combine results from all workers
    # r = []
    # for worker in workers:
    #     r.extend(worker.results)
    # return r
