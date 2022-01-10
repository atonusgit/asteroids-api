import json
import unittest

from .context import asteroid


class TestAsteroid(unittest.TestCase):

    @staticmethod
    def get_temp_file() -> dict:
        with open("tests/response.json", "r", encoding="utf8") as file:
            data = json.load(file)
            return data

    def test_get_closest(self):
        # given
        n = asteroid.Asteroid()
        temp_file = self.get_temp_file()["near_earth_objects"]

        # when
        result = n.get_closest(temp_file)

        # then
        self.assertTrue(isinstance(result, dict))

    def test_get_largest(self):
        # given
        n = asteroid.Asteroid()
        temp_file = self.get_temp_file()["near_earth_objects"]

        # when
        result = n.get_largest(temp_file)

        # then
        self.assertTrue(isinstance(result, dict))
