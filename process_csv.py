import csv
import json



def process_csv(destination, losses):
    processed_dict = {}

    with open(losses) as file:
        csvReader = csv.DictReader(file)
        for row in csvReader:
            if row["username"] != "username":
                row.pop("degree")
                processed_dict.update({
                    row["username"]: {
                        "next_player": row["next_player"]
                        }
                    })

    with open(destination, "w") as file:
        json.dump(processed_dict, file)

if __name__ == "__main__":
    process_csv("./json/bullet.json", "./data/final/1-bullet.csv")