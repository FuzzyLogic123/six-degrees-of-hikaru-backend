from fastapi import FastAPI
from typing import Optional

app = FastAPI()
item_set = set()

@app.post("/add_item/")
def add_item(item: str):
    item_set.add(item)
    return {"message": "Item added successfully", "statusCode": 200}

@app.get("/query_item/{item}")
def query_item(item: str):
    if item in item_set:
        return {"message": "Item exists", "statusCode": 200}
    else:
        return {"message": "Item does not exist", "statusCode": 502}
