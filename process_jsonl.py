import jsonlines
import json

def process_jsonl(destination, failed, losses):
    processed_dict = {}

    with open(losses) as reader:
        for obj in reader:
            obj = json.loads(obj)

            # if len(obj) != 1:
            #     raise Exception("Dict has more than one key")
            for player in obj:
                parent_player = player

            for child_player in obj[parent_player]["losses"]:
                if not processed_dict.get(child_player):
                    processed_dict[child_player] = {
                        "next_player": parent_player,
                        "degree": obj[parent_player]["degree"]
                    }

    with open(destination, "w") as file:
        json.dump(processed_dict, file)

    with open(failed) as file:
        for line in file:
            obj = json.loads(line)

            for player in obj:
                # if obj[player]:
                    print(obj[player])