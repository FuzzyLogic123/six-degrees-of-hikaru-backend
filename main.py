import json
from get_request_urls import get_request_urls
from get_player_losses import get_player_losses
from process_csv import process_csv
import csv

degree = 1
TIME_CONTROL = "bullet"
URL_LOCATION = './data/request_urls.txt'


# player losses is a dict: key is player, value is a dictionary with one key 'losses' which is a list of strings containing players that they have lost to
def writeToCsv(player_losses, degree):
    filename = f'./data/{TIME_CONTROL}.csv'
    data = []
    for player_that_lost in player_losses:
        for player_that_won in player_losses[player_that_lost]["losses"]:
            data.append([player_that_won, player_that_lost, degree])

    with open(filename, 'a', newline="") as file:
        if degree == 1:
            file.write('username,next_player,degree')

        for line in data:
            file.write(f'\n{line[0]},{line[1]},{line[2]}')


player_losses = get_player_losses(URL_LOCATION)
writeToCsv(player_losses, degree)

root_set = set()
for player in player_losses:
    root_set.update(player_losses[player]["losses"])
root = list(root_set)

with open('./data/root.json', 'w') as file:
    json.dump(root, file)