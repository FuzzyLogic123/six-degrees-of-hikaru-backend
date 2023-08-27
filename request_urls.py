import json
import queue
import random
import time
import urllib.request
from fileinput import filename
from threading import Thread
import json
import requests
from rich import print
from rich.console import Console
from rich.progress import track

from config import URL_LOCATION, MAX_CONCURRENT_REQUESTS, DEGREE, TIME_CONTROL, IS_FAILURES


def get_archive_urls():
    if IS_FAILURES:
        filename = f'{URL_LOCATION}/url_fetch_failures.txt'
    else:
        filename = f"./data/{TIME_CONTROL}/{DEGREE - 1}/results.csv"
    with open(filename, 'r') as file:
        file.readline() # skip header
        urls = []
        for line in file:
            if IS_FAILURES:
                urls += [line.strip()]
            else:
                player_username = line.split("|")[0]
                urls += [f"https://nlfezg5oid35cygimbmnxcsnee0ehmgk.lambda-url.us-west-1.on.aws/?url=https://api.chess.com/pub/player/{player_username}/games/archives&username={player_username}"]

    perform_web_requests(urls, MAX_CONCURRENT_REQUESTS)

#class for doing multiple requests at once
def perform_web_requests(addresses, no_workers):
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
                    t0 = time.time()
                    request = urllib.request.Request(content)
                    response = urllib.request.urlopen(request)

                    if response.getcode() != 200:
                        raise Exception(f"Error fetching chess.com archive: {response.getcode()}")

                    response = json.loads(response.read())
                    for archive in response["archives"]:
                        self.results += [f"{response['username']}|{TIME_CONTROL}|{archive}"]
                    self.queue.task_done()
                    print(f"[green]{content} {round(time.time() - t0, 1)}")
                except Exception as e:
                    # print(e)
                    print(f"[red]{content}")
                    with open(f'{URL_LOCATION}/url_fetch_failures.txt', 'a') as file:
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
    r = []
    for worker in workers:
        r.extend(worker.results)
    with open(f'{URL_LOCATION}/requests.txt', 'a') as file:
        for result in r:
            file.write(result + "\n")
