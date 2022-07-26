from wsgiref.simple_server import demo_app
from fastapi import FastAPI, HTTPException

from .main import search_title, get_content_advisory, get_info_by_id

app = FastAPI()


@app.get("/")
def read_index():
    return {"msg": "OK"}


@app.get("/search")
def search_titles(search_query: str):
    try:
        return {"results": search_title(query=search_query)}
    except:
        HTTPException(status_code=500, detail="Couldn't connect to servers")


@app.get("/advisory/{imdb_id}")
def read_content_advisory(imdb_id: str):
    try:
        return {"parental_guide": get_content_advisory(imdb_id)}
    except:
        raise HTTPException(status_code=500, detail="Unsuccessful request")


@app.get("/title/{tmdb_id}")
def read_title_info(tmdb_id: int):
    try:
        return {"results": get_info_by_id(tmdb_id=tmdb_id)}
    except:
        HTTPException(status_code=500, detail="Couldn't connect to servers")
