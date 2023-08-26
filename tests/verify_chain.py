import requests
import random

TIME_CLASS = "bullet"
DEGREE = 3


def has_player_lost(player_that_lost, archives_of_winner, time_class):
    for archive in archives_of_winner:
        archive = requests.get(archive).json()
        for game in archive["games"]:
            if game["time_class"] == time_class and game["rules"] == "chess":
                for colour in ("white", "black"):  #iterate over the black and white players
                    result = game[colour]["result"]
                    opponent_username = game[colour]["username"].lower()
                    if result in ("checkmated", "timeout", "resigned", "lose", "abandoned") and opponent_username == player_that_lost:
                        return True
    return False

with open(f"./data/{TIME_CLASS}/{DEGREE}/results.csv", "r") as file:

    for line in file:
        if random.random() > 0.00001:
            continue

        username, next_player, degree = line.split("|")
        username = username.lower()
        if username == "username":
            continue
        
        print(f"checking {username} vs {next_player}", end="\r")
        archives = requests.get(f"https://api.chess.com/pub/player/{username}/games/archives").json()["archives"]
        if not has_player_lost(next_player, archives, TIME_CLASS):
            raise Exception(f"{next_player} did not lose to {username}")
        else:
            print(f"{next_player} lost to {username}")

