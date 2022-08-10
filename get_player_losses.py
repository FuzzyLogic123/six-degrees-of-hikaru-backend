from fileinput import filename
import requests
import time
import json
from rich.progress import track
import jsonlines
from rich.console import Console

import queue, time, urllib.request
from threading import Thread

# losses = []

def get_player_losses(path_to_request_list, lossesSaveLocation, failuresSaveLocation, degree):

    with open(path_to_request_list) as file:
        urls = []
        for line in file:
            urls += [line]


    perform_web_requests(urls, 16, lossesSaveLocation, failuresSaveLocation, degree)
    return losses




#class for doing multiple requests at once
def perform_web_requests(addresses, no_workers, lossesSaveLocation, failuresSaveLocation, degree):
    class Worker(Thread):
        def __init__(self, request_queue):
            Thread.__init__(self)
            self.queue = request_queue
            self.results = []

        def run(self):
            while True:
                content = self.queue.get()
                if content == "":
                    break
                try:
                    request = urllib.request.Request(content)
                    response = urllib.request.urlopen(request)

                    #process data
                    losses_set = set()
                    failed_requests = []
                    result = json.loads(response.read())
                    print(result)
                    if result["failed_requests"]:
                        failed_requests.append(result["failed_requests"])
                    else:
                        losses_set.update(result["player_losses"])
                        losses += result["player_losses"] #move this to another function maybe
                    player_username = result["player"]
                    write_to_file(lossesSaveLocation, list(losses_set), player_username, degree)
                    write_to_file(failuresSaveLocation, failed_requests, player_username)

                    self.results.append(response.read())
                    self.queue.task_done()
                except Exception as e:
                    print(e)
                    time.sleep(5)


    # Create queue and add addresses
    q = queue.Queue()
    for url in addresses:
        q.put(url)

    # Workers keep working till they receive an empty string
    for _ in range(no_workers):
        q.put("")

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
    return r

def write_to_file(filename, losses, player_username, degree):

    with jsonlines.open(filename, 'a') as writer:
        player_json = {
            player_username: losses,
            "degree": degree
        }

        # console.print(player_json)

        writer.write(player_json)