import json

dict = {}

with open("./json/blitz.json") as file:
    dict["blitz"] = json.load(file)

with open("./json/bullet.json") as file:
    dict["bullet"] = json.load(file)

with open("./json/final.json", "w") as file:
    json.dump(dict, file)
