from fileinput import filename
import requests
import time
import json
from rich.progress import track
import jsonlines
from rich.console import Console

import queue, time, urllib.request
from threading import Thread

player_losses = {}

def get_player_losses(path_to_request_list):

    with open(path_to_request_list) as file:
        urls = []
        for line in file:
            urls += [line]



    perform_web_requests(urls, 16)
    return player_losses




#class for doing multiple requests at once
def perform_web_requests(addresses, no_workers):
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
                    result = json.loads(response.read())
                    current_player = result["player"]
                    if not player_losses.get(current_player):
                        player_losses[current_player] = {
                            "losses": set(),
                            "failed_requests": set()
                        }
                    else:
                        player_losses[current_player]["losses"].update(result["player_losses"])
                        player_losses[current_player]["failed_requests"].update(result["failed_requests"])
                        print(player_losses)

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

# def write_to_file(filename, losses, player_username, degree):

#     with jsonlines.open(filename, 'a') as writer:
#         player_json = {
#             player_username: losses,
#             "degree": degree
#         }

#         # console.print(player_json)

#         writer.write(player_json)
