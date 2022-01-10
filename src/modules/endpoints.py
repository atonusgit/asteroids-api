from fastapi import FastAPI

import globals_vars
from cache import Cache
from asteroid import Asteroid

app = FastAPI(
    title="Asteroids API",
    description="Deliver asteroid info from Nasa API. See the detailed explanation in README.md via github link.",
    version="0.0.1",
    contact={
        "name": "Anton Valle",
        "url": "https://github.com/atonusgit/asteroids-api"
    },
)
cache = Cache()
asteroid = Asteroid()


@app.get("/")
def root():
    return [globals_vars.root_msg]


@app.get("/show-closest-asteroid")
def show_closest_asteroid():
    return asteroid.get_closest_asteroid()


@app.get("/show-largest-asteroid")
def show_largest_asteroid(year: int):
    return asteroid.get_largest_asteroid(year)


@app.get("/show-cache")
def show_cache():
    return globals_vars.cache


@app.get("/reset-cache")
def reset_cache(purge: bool = False):
    globals_vars.cache = {}
    if purge:
        cache.delete_cache_file()
    return globals_vars.cache
