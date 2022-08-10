from get_request_urls import get_request_urls
from get_player_losses import get_player_losses
from process_jsonl import process_jsonl

root = ["hikaru"]

DEGREES_LIMIT = 2
TIME_CONTROL = "bullet"
URL_LOCATION = './data/request_urls/1.txt'
URL_FAIL_LOCATION = './data/request_urls/fail.txt'
LOSSES_SAVE_LOCATION = './data/player_losses/1.jsonl'
FAILURES_SAVE_LOCATION = './data/player_losses/failed_requests.jsonl'

DESTINATION = './data/final/1.jsonl'

for degree in range(DEGREES_LIMIT):
    get_request_urls(root, TIME_CONTROL, URL_LOCATION, URL_FAIL_LOCATION)
    root = get_player_losses(URL_LOCATION, LOSSES_SAVE_LOCATION, FAILURES_SAVE_LOCATION, degree)

process_jsonl(DESTINATION, FAILURES_SAVE_LOCATION, LOSSES_SAVE_LOCATION)

