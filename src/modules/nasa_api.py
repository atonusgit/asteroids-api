import os
import cache
import globals_vars
from isoweek import Week
import concurrent.futures
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from requests import Request, Session, Response

load_dotenv()
cache = cache.Cache()


class NasaApi:
    _ENDPOINT = 'https://api.nasa.gov/neo/rest/v1/'

    def __init__(self):
        self.closest_asteroid = {
            "date": "",
            "index": 0,
            "miss_distance": 10000000000
        }
        self.largest_asteroid = {
            "date": "",
            "index": 0,
            "estimated_diameter_max": 0
        }
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

    def get_closest(self, near_earth_objects: dict) -> dict:

        # go through each day and each asteroid item in a day
        for near_earth_object in near_earth_objects:
            for index, i in enumerate(near_earth_objects[near_earth_object]):

                # go through each close_approach_data item and make sure miss_distance key is found
                for sub_index, close_approach_data in enumerate(i["close_approach_data"]):
                    if close_approach_data.get('miss_distance', False) is not False:

                        # overwrite self.closest_asteroid if closer miss_distance is found
                        if float(self.closest_asteroid["miss_distance"]) > float(i["close_approach_data"][sub_index]["miss_distance"]["kilometers"]):
                            self.closest_asteroid = {
                                "date": near_earth_object,
                                "index": index,
                                "miss_distance": i["close_approach_data"][sub_index]["miss_distance"]["kilometers"]
                            }

        return near_earth_objects[self.closest_asteroid["date"]][self.closest_asteroid["index"]]

    def get_closest_asteroid(self) -> dict:
        start_date = "2015-12-19"
        end_date = "2015-12-26"

        data = self.call_via_cache(
            "dates", "feed", start_date, end_date, "near_earth_objects")

        closest_item = self.get_closest(data)
        closest_item_details = self.get_asteroid_details(closest_item["id"])

        return closest_item_details

    def remove_days_from_other_years(self, year: int, near_earth_objects: dict) -> dict:
        for near_earth_object in near_earth_objects.copy().items():
            if str(year) not in near_earth_object[0]:
                near_earth_objects.pop(near_earth_object[0])

        return near_earth_objects

    def get_all_asteroids_of_year(self, year: int) -> dict:
        w1 = Week(year, 0)
        near_earth_objects = dict()
        calls_params = list()

        for i in range(w1.last_week_of_year(year).week + 1):
            w2 = Week(year, 0) + i
            start_date = w2.days()[0].strftime('%Y-%m-%d')
            end_date = w2.days()[-1].strftime('%Y-%m-%d')
            calls_params.append(["dates", "feed", start_date,
                                 end_date, "near_earth_objects"])

        with concurrent.futures.ThreadPoolExecutor(max_workers=53) as executor:
            futures = [executor.submit(lambda p: self.call_via_cache(
                *p), call_params) for call_params in calls_params]

            for f in futures:
                near_earth_objects = near_earth_objects | f.result()

        near_earth_objects = self.remove_days_from_other_years(
            year, near_earth_objects)

        return near_earth_objects

    def get_largest(self, near_earth_objects: dict) -> dict:
        self.largest_asteroid = {
            "date": "",
            "index": 0,
            "estimated_diameter_max": 0
        }

        # go through each day and each asteroid item in a day
        for near_earth_object in near_earth_objects:
            for index, i in enumerate(near_earth_objects[near_earth_object]):

                # make sure meters key is found
                if i["estimated_diameter"].get('meters', False) is not False:

                    # overwrite self.largest_asteroid if larger estimated_diameter_max is found
                    if float(self.largest_asteroid["estimated_diameter_max"]) < float(i["estimated_diameter"]["meters"]["estimated_diameter_max"]):
                        self.largest_asteroid = {
                            "date": near_earth_object,
                            "index": index,
                            "estimated_diameter_max": i["estimated_diameter"]["meters"]["estimated_diameter_max"]
                        }

        return near_earth_objects[self.largest_asteroid["date"]][self.largest_asteroid["index"]]

    def get_largest_asteroid(self, year: int) -> dict:
        near_earth_objects = self.get_all_asteroids_of_year(year)
        largest_item = self.get_largest(near_earth_objects)
        largest_item_details = self.get_asteroid_details(largest_item["id"])

        return largest_item_details

    def get_asteroid_details(self, asteroid_id: int) -> dict:
        asteroid_details = self.call_via_cache(
            "singles", 'neo/' + asteroid_id, asteroid_id)
        return asteroid_details

    def call_via_cache(self, type: str, path: str, key: str, end_date: Optional[str] = None, data_key: Optional[str] = None) -> Any:

        if globals_vars.cache.get(type, False) is False:
            globals_vars.cache[type] = dict()

        if key in globals_vars.cache[type]:
            if type is "singles":
                data = globals_vars.cache[type][key]
            else:
                data = globals_vars.cache[type]
        else:
            data = self._call(path, key, end_date)

            if data_key:
                globals_vars.cache[type] = globals_vars.cache[type] | data[data_key]
                data = data[data_key]
            else:
                globals_vars.cache[type][key] = data

        cache.save_cache_file(globals_vars.cache)
        return data
