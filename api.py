import json
import redis
from datetime import timedelta
from fastapi import FastAPI, HTTPException

from main import search_title, get_content_advisory, get_info_by_id

app = FastAPI()


REDIS_SERVER_PORT = 6379


@app.get("/")
def read_index():
    return {"msg": "OK"}


@app.get("/search")
def search_titles(search_query: str):
    try:
        return {"results": search_title(query=search_query)}
    except:
        HTTPException(status_code=500, detail="Couldn't connect to servers")


@app.get("/advisory/{tmdb_id}")
def read_content_advisory(tmdb_id: int):
    try:
        title_info = get_info_by_id(tmdb_id=tmdb_id)
        imdb_id = title_info["imdb_id"]

        # Checking the Redis cache first
        redis_client = redis.Redis(host="localhost", port=REDIS_SERVER_PORT, db=0)

        response_body = {
            "title": title_info["title"],
            "id": tmdb_id,
            "imdb_id": imdb_id,
            "parental_guide": {},
        }

        parental_guide = redis_client.get(imdb_id)
        if parental_guide:
            print("Cache hit")
            response_body["parental_guide"] = json.loads(parental_guide)
            return response_body

        print("Cache miss")

        # Scraping since cache miss
        parental_guide = get_content_advisory(imdb_id)

        # Saving results in cache for quick future retrieval
        redis_client.set(imdb_id, json.dumps(parental_guide))
        redis_client.expire(imdb_id, timedelta(minutes=15))

        return response_body
    except:
        raise HTTPException(status_code=500, detail="Unsuccessful request")


@app.get("/title/{tmdb_id}")
def read_title_info(tmdb_id: int):
    try:
        return {"results": get_info_by_id(tmdb_id=tmdb_id)}
    except:
        HTTPException(status_code=500, detail="Couldn't connect to servers")
