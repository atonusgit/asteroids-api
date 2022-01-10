import json
import unittest

from .context import helpers


class TestHelpers(unittest.TestCase):

    @staticmethod
    def get_temp_file() -> dict:
        with open("tests/response.json", "r", encoding="utf8") as file:
            data = json.load(file)
            return data

    def test_remove_days_from_other_years(self):
        # given
        temp_file = self.get_temp_file()["near_earth_objects"]

        # when
        result = helpers.remove_days_from_other_years(
            2015, temp_file)

        # then
        self.assertFalse("2016-01-02" in result.keys())
        self.assertTrue("2015-12-25" in result.keys())
