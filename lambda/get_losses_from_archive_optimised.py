import requests
import time

def get_request(url, attempts_remaining = 3):
    if attempts_remaining == 0:
        return False
    try:
        request = requests.get(url, timeout=5)
        return request.json()
    except:
        time.sleep(0.25)
        print("retrying...")
        return get_request(url, attempts_remaining - 1)
        


def lambda_handler(event, context):
    player_losses = set()
    response_dict  = {}
    player_username = event["queryStringParameters"]["username"].lower()
    time_class = event["queryStringParameters"]["time_class"]
    request_url = event["queryStringParameters"]["url"]
    t1 = time.time()
    archive = get_request(request_url)
        
    if archive == False or archive.get("games") == None:
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
                    player_losses.add(opponent_username)
    

    cached_result = requests.post("http://54.176.0.0:5000/query_items/", json=list(player_losses)).json()["body"]

    cheaters = cached_result["cheaters_list"]
    fair_players = cached_result["fair_players_list"]

    for cheater in cheaters:
        player_losses.remove(cheater)

    fair_play_abusers = set()
    for player in player_losses:
        if player not in fair_players:
            response = requests.get(f"https://api.chess.com/pub/player/{player}").json()
            if response.get("status") == "closed:fair_play_violations" or response.get("status") == None: # if the user doesn't exist then don't add them to the list
                fair_play_abusers.add(player)

    for player in fair_play_abusers:
        player_losses.remove(player)

    requests.post("http://54.176.0.0:5000/add_cheaters/", json=list(fair_play_abusers))
    requests.post("http://54.176.0.0:5000/add_fair_players/", json=list(player_losses))

    response_dict["player_losses"] = list(player_losses)
    response_dict["player"] = player_username
    print(time.time() - t1)
    return {
        'statusCode': 200,
        'body': response_dict
    }

# https://iaprgyb7j4t7ymppwyzewul5ei0wfrqp.lambda-url.us-west-1.on.aws/?time_class=bullet&url=https://api.chess.com/pub/player/aaahameed/games/2022/02&username=aaahameed
print(lambda_handler({"queryStringParameters": {"username": "aaahameed", "time_class": "bullet", "url": "https://api.chess.com/pub/player/aaahameed/games/2022/02"}}, None))