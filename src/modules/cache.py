import os
import json
import pathlib

import globals_vars

#
#   Cache has two parts - dict and json file.
#   The cache.json, if available, is loaded to
#   dict at start.
#
#   Handling cache dict is done with public
#   function nasa_api.call_via_cache()
#


class Cache:
    _CACHE_FILE = str(pathlib.Path(
        __file__).parent.resolve()) + "/../cache.json"

    def __init__(self):
        globals_vars.cache = self.get_cache_file()

    def save_cache_file(self, data):
        with open(self._CACHE_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def get_cache_file(self):
        try:
            with open(self._CACHE_FILE, "r") as file_data:
                return json.load(file_data)
        except:
            return {}

    def delete_cache_file(self):
        if os.path.exists(self._CACHE_FILE):
            os.remove(self._CACHE_FILE)
