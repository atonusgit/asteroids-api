import os
import json
import pathlib
import globals_vars


class Cache:
    def __init__(self):
        globals_vars.cache = self.get_cache_file(
            str(pathlib.Path(__file__).parent.resolve()) + "/../cache.json")

    def save_cache_file(self, data, filename=str(pathlib.Path(__file__).parent.resolve()) + "/../cache.json"):
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    def get_cache_file(self, filename):
        try:
            with open(filename, "r") as file_data:
                return json.load(file_data)
        except:
            return {}

    def delete_cache_file(self, filename=str(pathlib.Path(__file__).parent.resolve()) + "/../cache.json"):
        if os.path.exists(filename):
            os.remove(filename)
