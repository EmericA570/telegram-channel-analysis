import json
import os

import requests
import uvicorn
from fastapi import FastAPI, HTTPException

from osn_scrap.helper import extract_messages
from osn_scrap.schemas import Message

app = FastAPI()


@app.get("/query/")
def get_list_of_stored_queries() -> list[str]:
    return os.listdir("./query/")


@app.post("/query/{query_id}")
def get_messages_from_channel(query_id: str, channel: str) -> list[Message]:
    if os.path.exists(f"./query/{query_id}.json"):
        raise HTTPException(status_code=403, detail="A query already has this name")

    url = f"https://t.me/s/{channel}"
    response = requests.get(url=url)

    response = extract_messages(response)

    with open(f"./query/{query_id}.json", "w") as file:
        json.dump(response, file)

    return response


@app.get("/query/{query_id}")
def get_messages_from_json(query_id: str):
    try:
        with open(f"./query/{query_id}.json", "r") as file:
            query = json.load(file)
        return query
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Query not found")


@app.delete("/query/{query_id}")
def remove_messages(query_id: str):
    if not os.path.exists(f"./query/{query_id}.json"):
        raise HTTPException(status_code=404, detail="Query not found")

    os.remove(f"./query/{query_id}.json")


if __name__ == "__main__":
    if not os.path.isdir("./query"):
        os.mkdir("./query")

    uvicorn.run(app="main:app", reload=True)
