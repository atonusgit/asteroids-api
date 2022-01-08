import os
import json
import unittest
from .context import nasa_api
import sys


class TestNasaApi(unittest.TestCase):

    @staticmethod
    def get_temp_file() -> dict:
        with open("tests/response.json", "r", encoding="utf8") as file:
            data = json.load(file)
            return data

    # def test_feed(self):
    #     n = nasa_api.NasaApi()
    #     result = n._feed()
    #     self.assertEqual(str(list(result.keys())[0]), 'links')

    def test_get_closest(self):
        n = nasa_api.NasaApi()
        result = n.get_closest(self.get_temp_file()["near_earth_objects"])
        self.assertTrue(isinstance(result, dict))

    def test_remove_days_from_other_years(self):
        n = nasa_api.NasaApi()
        result = n.remove_days_from_other_years(
            2015, self.get_temp_file()["near_earth_objects"])
        self.assertFalse("2016-01-02" in result.keys())
        self.assertTrue("2015-12-25" in result.keys())

    def test_get_largest(self):
        n = nasa_api.NasaApi()
        result = n.get_largest(self.get_temp_file()["near_earth_objects"])
        self.assertTrue(isinstance(result, dict))
