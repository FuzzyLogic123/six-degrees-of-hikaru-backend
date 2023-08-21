import requests
import time
import json

def get_request(url, attempts_remaining = 2):
    if attempts_remaining == 0:
        return False
    try:
        request = requests.get(url)
        return request.json()
    except:
        time.sleep(3)
        return get_request(url, attempts_remaining - 1)
        


def lambda_handler(event, context):
    player_losses = set()
    response_dict  = {}
    player_username = event["queryStringParameters"]["username"].lower()
    time_class = event["queryStringParameters"]["time_class"]
    request_url = event["queryStringParameters"]["url"]
    request_time = 0
    requests_count = 0
    t2 = time.time()
    archive = get_request(request_url)
    requests_count += 1
    request_time += time.time() - t2
    print(time.time() - t2)
    
    if archive == False:
        return {
            'statusCode': 500,
            'body': 'Error fetching chess.com archive'
        }

    for game in archive["games"]:
        if game["time_class"] == time_class and game["rules"] == "chess":
            for colour in ("white", "black"):  #iterate over the black and white players
                result = game[colour]["result"]
                opponent_username = game[colour]["username"].lower()
                if result == "win" and opponent_username != player_username:
                    t2 = time.time()
                    fair_play_status = get_request(f"https://api.chess.com/pub/player/{opponent_username}")["status"]
                    request_time += time.time() - t2
                    requests_count += 1
                    if fair_play_status == False:
                        return {
                            'statusCode': 500,
                            'body': f"failed to get fair play status for {opponent_username}"
                        }
                    elif fair_play_status != "closed:fair_play_violations":
                        player_losses.add(opponent_username)
                    else:
                        print("fair play abuser")
                        print(opponent_username)
    response_dict["player_losses"] = list(player_losses)
    response_dict["player"] = player_username
    return {
        'statusCode': 200,
        'body': response_dict
    }

# print(lambda_handler({"queryStringParameters": {"username": "thecarefulcactus", "time_class": "blitz", "url": "https://api.chess.com/pub/player/thecarefulcactus/games/2021/09"}}, None))