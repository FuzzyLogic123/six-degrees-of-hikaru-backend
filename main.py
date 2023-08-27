from config import TIME_CONTROL, DEGREE, URL_LOCATION, IS_FAILURES, IS_GET_URLS
from api import get_player_losses
from request_urls import get_archive_urls


# player losses is a dict: key is player, value is a dictionary with one key 'losses' which is a list of strings containing players that they have lost to
def writeToCsv(player_losses, degree):
    filename = f'{URL_LOCATION}/results.csv'
    data = []
    for player_that_lost in player_losses:
        for player_that_won in player_losses[player_that_lost]["losses"]:
            data.append([player_that_won, player_that_lost, degree])

    with open(filename, 'a', newline="") as file:
        if not IS_FAILURES:
            file.write('username|next_player|degree\n')

        for line in data:
            file.write(f'{line[0]}|{line[1]}|{line[2]}\n')

if IS_GET_URLS:
    get_archive_urls()
else:
    player_losses = get_player_losses()
    writeToCsv(player_losses, DEGREE)