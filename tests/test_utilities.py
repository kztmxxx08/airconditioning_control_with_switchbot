import unittest

from src import utilities


class Utilities(unittest.TestCase):
    def test_load_setting_file(self):
        test_setting_result = utilities.load_setting_file()
        self.assertIsInstance(test_setting_result, dict)
        self.assertIn("switchbot", test_setting_result)
        self.assertIn("HomeControl", test_setting_result)
        self.assertIn("TableName", test_setting_result)

    def test_define_datetime_dict(self):
        test_time_result = utilities.define_datetime_dict()
        self.assertIsInstance(test_time_result, dict)
        self.assertIn("now", test_time_result)
        self.assertIn("date_year_month_day", test_time_result)
        self.assertIn("time_hour_minutes", test_time_result)
