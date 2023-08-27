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
    request_url = event["queryStringParameters"]["url"]
    request_time = 0
    requests_count = 0
    t2 = time.time()
    archive = get_request(request_url)
    requests_count += 1
    request_time += time.time() - t2
    print(time.time() - t2)
        
    if archive == False or archive.get("archives") == None:
        return {
            'statusCode': 500,
            'body': 'Error fetching chess.com archive'
        }
    return {
        'statusCode': 200,
        'body': archive["archives"]
    }


print(lambda_handler({"queryStringParameters": {"url": "https://api.chess.com/pub/player/erik/games/archives"}}, None))