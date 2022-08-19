# isAdult: Instant Content Advisory

## Find out if your child should be watching that movie

### Introduction

isAdult is a tiny microservice that scrapes the web to provide you with parental warnings about any movie or TV show. So no more sitting on the edge of your seat, anxiously gawking for sudden awkward scenes, ready to flee or hide your kid's eyes the next time you are watching something with the whole family.

Simply search for the title, instantly get a summary of the parental guide, and decide for yourself if the title is okay to watch.

### Why did I make it?

Honestly? I just wanted to learn a few skills. And this seemed like a good enough idea to try them out :P

### How to use it?
Make sure to have Python, Redis, and Docker installed on your system.

Clone the repo, install the dependencies, and then start the FastAPI server 🎈

Oh, and make sure to get your TMDB API key and add it to a `.env` file at the root directory under the key `TMDB_API_KEY`
