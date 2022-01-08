import cache
import nasa_api
import globals_vars
from fastapi import FastAPI

n = nasa_api.NasaApi()
app = FastAPI()
cache = cache.Cache()


@app.get("/")
def hello():
    return {"Hello world!"}


@app.get("/show-closest-asteroid")
def show_closest_asteroid():
    return n.get_closest_asteroid()


@app.get("/show-largest-asteroid")
def show_largest_asteroid(year: int = 2023):
    return n.get_largest_asteroid(year)


@app.get("/show-cache")
def show_cache():
    return globals_vars.cache


@app.get("/reset-cache")
def reset_cache(purge: bool = False):
    globals_vars.cache = {}
    if purge:
        cache.delete_cache_file()
    return globals_vars.cache
