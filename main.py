from get_request_urls import get_request_urls
from get_player_losses import get_player_losses
from process_jsonl import process_jsonl
import csv

root = ["Hikaru"]

DEGREES_LIMIT = 2
TIME_CONTROL = "bullet"
URL_LOCATION = './data/request_urls/1.txt'
# URL_FAIL_LOCATION = './data/request_urls/fail.txt'
# LOSSES_SAVE_LOCATION = './data/player_losses/1.jsonl'
# FAILURES_SAVE_LOCATION = './data/player_losses/failed_requests.jsonl'

DESTINATION = './data/final/1.csv'

def writeToCsv(player_losses, degree):
    filename = DESTINATION
    header = ['username', 'next_player', 'degree']
    data = []
    for player_that_lost in player_losses:
        for player_that_won in player_losses[player_that_lost]["losses"]:
            data.append([player_that_won, player_that_lost, degree])

    with open(filename, 'w', newline="") as file:
        csvwriter = csv.writer(file) # 2. create a csvwriter object
        csvwriter.writerow(header) # 4. write the header
        csvwriter.writerows(data) # 5. write the rest of the data


for degree in range(DEGREES_LIMIT):
    failed_requests = get_request_urls(root, TIME_CONTROL, URL_LOCATION)
    print(failed_requests)
    player_losses = get_player_losses(URL_LOCATION)
    writeToCsv(player_losses, degree)

    root_set = set()
    for player in player_losses:
        root_set.update(player_losses[player]["losses"])
    root = list(root_set)

