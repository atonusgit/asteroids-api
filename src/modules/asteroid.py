import concurrent.futures
from datetime import date
from isoweek import Week

import helpers
from nasa_api import NasaApi

nasa_api = NasaApi()


class Asteroid:
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

    #
    #   Get asteroids from /feed endpoint with
    #   fixed dates and return the closest one
    #
    def get_closest_asteroid(self) -> dict:
        start_date = date(2015, 12, 19)
        end_date = date(2015, 12, 26)

        data = nasa_api.call_via_cache(
            "dates", "feed", start_date.isoformat(), end_date.isoformat(), "near_earth_objects")

        data = helpers.remove_days_outside_scope(data, start_date, end_date)
        closest_item = self.get_closest(data)
        closest_item_details = self.get_asteroid_details(closest_item["id"])

        return closest_item_details

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

    #
    #   Get asteroids from /feed endpoint by
    #   year and return the largest one
    #
    def get_largest_asteroid(self, year: int) -> dict:
        near_earth_objects = self.get_all_asteroids_of_year(year)
        largest_item = self.get_largest(near_earth_objects)
        largest_item_details = self.get_asteroid_details(largest_item["id"])

        return largest_item_details

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

    #
    #   Make concurrent requests to Nasa API.
    #   Nasa allows max 7 days at once and
    #   max 10 concurrent requests
    #
    def get_all_asteroids_of_year(self, year: int) -> dict:
        w1 = Week(year, 0)
        near_earth_objects = dict()
        calls_params = list()

        for i in range(w1.last_week_of_year(year).week + 1):
            w2 = Week(year, 0) + i
            start_date = w2.days()[0].isoformat()
            end_date = w2.days()[-1].isoformat()
            calls_params.append(["dates", "feed", start_date,
                                 end_date, "near_earth_objects"])

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(lambda p: nasa_api.call_via_cache(
                *p), call_params) for call_params in calls_params]

            for f in futures:
                near_earth_objects = near_earth_objects | f.result()

        near_earth_objects = helpers.remove_days_from_other_years(
            year, near_earth_objects)

        return near_earth_objects

    #
    #   Get details of a single asteroid from /neo endpoint
    #
    def get_asteroid_details(self, asteroid_id: int) -> dict:
        asteroid_details = nasa_api.call_via_cache(
            "singles", 'neo/' + asteroid_id, asteroid_id)
        return asteroid_details
