import json
import queue
import time
import urllib.request
from fileinput import filename
from threading import Thread
import json
import jsonlines
import requests
from rich import print
from rich.console import Console
from rich.progress import track

player_losses = {}

def get_player_losses(path_to_request_list):

    with open(path_to_request_list, 'r+') as file:
        urls = []
        for line in file:
            urls += [line]
        file.truncate(0)
        file.seek(0)

    perform_web_requests(urls, 50)
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
                    player_losses[current_player]["losses"].update(result["player_losses"])
                    self.results.append(response.read())
                    self.queue.task_done()
                    print(f"[green]{current_player}")
                except Exception as e:
                    print(f"[red]{e}")
                    print(f"[red]{content}")
                    with open('./data/request_urls/failures.txt', 'a') as file:
                        file.write(content)

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

# def write_to_file(filename, losses, player_username, degree):

#     with jsonlines.open(filename, 'a') as writer:
#         player_json = {
#             player_username: losses,
#             "degree": degree
#         }

#         # console.print(player_json)

#         writer.write(player_json)
