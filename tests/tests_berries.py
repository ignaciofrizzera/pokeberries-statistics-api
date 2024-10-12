from berries.service import BerriesService
from django.test import SimpleTestCase


class TestsBerries(SimpleTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.data = BerriesService().get_statistics()

    def test_has_data(self):
        self.assertIsNotNone(self.data)
        self.assertGreater(len(self.data["berries_names"]), 0)
    
    def test_data_keys(self):
        expected_keys = [
            "berries_names", "min_growth_time", "median_growth_time", 
            "max_growth_time", "variance_growth_time", "mean_growth_time", "frequency_growth_time"]
        for expected_key in expected_keys:
            self.assertIn(expected_key, self.data)
    
    def test_data_types(self):
        self.assertIsInstance(self.data, dict)
        self.assertIsInstance(self.data["berries_names"], list)
        for berry_name in self.data["berries_names"]:
            self.assertIsInstance(berry_name, str)
        self.assertIsInstance(self.data["min_growth_time"], int)
        self.assertIsInstance(self.data["median_growth_time"], float)
        self.assertIsInstance(self.data["max_growth_time"], int)
        self.assertIsInstance(self.data["variance_growth_time"], float)
        self.assertIsInstance(self.data["mean_growth_time"], float)
        self.assertIsInstance(self.data["frequency_growth_time"], int)
    
    def test_min_max_growth_time(self):
        self.assertLessEqual(self.data["min_growth_time"], self.data["max_growth_time"])
    
    def test_all_positive(self):
        self.assertGreaterEqual(self.data["min_growth_time"], 0)
        self.assertGreaterEqual(self.data["max_growth_time"], 0)
        self.assertGreater(self.data["median_growth_time"], 0)
        self.assertGreater(self.data["variance_growth_time"], 0)
        self.assertGreater(self.data["mean_growth_time"], 0)
    
    def test_frequency_in_range(self):
        frequency_growth_time = self.data["frequency_growth_time"]
        self.assertGreaterEqual(frequency_growth_time, self.data["min_growth_time"])
        self.assertLessEqual(frequency_growth_time, self.data["max_growth_time"])
    
    def test_unique_berries_names(self):
        berries_names = self.data["berries_names"]
        unique_names = set(berries_names)
        self.assertEqual(len(unique_names), len(berries_names))
    
    def test_all_equal_growth_times(self):
        if self.data["min_growth_time"] == self.data["max_growth_time"] or len(self.data["berries_names"]) == 1:
            self.assertEqual(self.data["min_growth_time"], self.data["max_growth_time"])
            self.assertEqual(self.data["max_growth_time"], self.data["frequency_growth_time"])
            self.assertEqual(self.data["max_growth_time"], int(self.data["mean_growth_time"]))
            self.assertEqual(self.data["max_growth_time"], int(self.data["median_growth_time"]))
            self.assertEqual(self.data["variance_growth_time"], 0.0)

    def test_mean_median_variance_rounding(self):
        rounded_mean = round(self.data["mean_growth_time"], 2)
        self.assertAlmostEqual(self.data["mean_growth_time"], rounded_mean, places=2)
        rounded_median = round(self.data["median_growth_time"], 2)
        self.assertAlmostEqual(self.data["median_growth_time"], rounded_median, places=2)
        rounded_variance = round(self.data["variance_growth_time"], 2)
        self.assertAlmostEqual(self.data["variance_growth_time"], rounded_variance, places=2)