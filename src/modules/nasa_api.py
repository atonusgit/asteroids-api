import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from requests import Request, Session, Response

import helpers
import globals_vars
from cache import Cache

load_dotenv()
cache = Cache()


class NasaApi:
    _ENDPOINT = 'https://api.nasa.gov/neo/rest/v1/'

    def __init__(self):
        self._nasa_api_key = os.getenv('NASA_API_KEY')
        self._session = Session()

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        print("request done")
        return self._request('GET', path, params=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        request = Request(method, self._ENDPOINT + path, **kwargs)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            return data

    def _call(self, path, start_date: Optional[str], end_date: Optional[str]) -> dict:
        params = {}
        if start_date:
            params["start_date"] = start_date

        if end_date:
            params["end_date"] = end_date

        params["api_key"] = self._nasa_api_key

        response = self._get(path, params)
        return response

    #
    #   Public function for making calls from other modules
    #
    def call_via_cache(self, top_key: str, path: str, key: str, end_date: Optional[str] = None, data_key: Optional[str] = None) -> Any:
        if globals_vars.cache.get(top_key, False) is False:
            globals_vars.cache[top_key] = dict()

        if key in globals_vars.cache[top_key]:
            if top_key == "singles":
                return globals_vars.cache[top_key][key].copy()
            else:
                return globals_vars.cache[top_key].copy()
        else:
            data = self._call(path, key, end_date)

            if data_key:
                reduced_data = helpers.reduce_response_data(data, data_key)
                globals_vars.cache[top_key] = globals_vars.cache[top_key] | reduced_data[data_key]
                data = reduced_data[data_key]
            else:
                globals_vars.cache[top_key][key] = data

            cache.save_cache_file(globals_vars.cache)

        return data
