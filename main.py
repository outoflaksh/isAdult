import os
import json
import redis
import requests
from datetime import timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup


def search_title(query: str):
    load_dotenv()

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

    URL = f"https://api.themoviedb.org/3/search/multi?api_key={TMDB_API_KEY}&query={query}"

    response = requests.get(url=URL).json()
    results = response["results"]

    return results


def get_info_by_id(tmdb_id: int):
    load_dotenv()

    TMDB_API_KEY = os.environ.get("TMDB_API_KEY")

    MOVIE_URL = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={TMDB_API_KEY}"

    response = requests.get(url=MOVIE_URL).json()

    return response


def get_content_advisory(imdb_id: str):
    result = {}
    ADV_URL = f"https://www.imdb.com/title/{imdb_id}/parentalguide"

    imdb_response = requests.get(url=ADV_URL)

    criterion = {
        "Sex & Nudity": "nudity",
        "Violence & Gore": "violence",
        "Profanity": "profanity",
        "Alcohol, Drugs & Smoking": "alcohol",
        "Frightening & Intense Scenes": "frightening",
    }

    if imdb_response.status_code == 200:
        soup = BeautifulSoup(imdb_response.content, "html.parser")
        for c in criterion:
            severity = (
                soup.find("section", {"id": f"advisory-{criterion[c]}"})
                .find("span", {"class": "ipl-status-pill"})
                .text
            )

            result[c] = severity

        return result
    else:
        raise Exception(f"Unsuccessful HTTP request on {ADV_URL}")
