from berries.service import BerriesService
from django.test import SimpleTestCase
from PIL.ImageFile import ImageFile
from PIL import Image
import base64
import io


class TestsBerries(SimpleTestCase):
    
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.service = BerriesService()
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

    def test_get_statistics_returns(self):
        no_visualization_data = self.service.get_statistics(for_visualization=False)
        self.assertIsInstance(no_visualization_data, dict)
        visualization_data = self.service.get_statistics(for_visualization=True)
        self.assertIsInstance(visualization_data, tuple)
        self.assertEqual(len(visualization_data), 2)
        statistics_data, growth_times = visualization_data[0], visualization_data[1]
        self.assertIsInstance(statistics_data, dict)
        self.assertIsInstance(growth_times, list)
    
    @staticmethod
    def __decode_image(encoded_image: str) -> ImageFile:
        decoded_bar_chart_image = base64.b64decode(encoded_image)
        return Image.open(io.BytesIO(decoded_bar_chart_image))

    def __test_image(self, encoded_image: str):
        image = self.__decode_image(encoded_image)
        self.assertIsNotNone(image)
        self.assertEqual(image.format, 'PNG')
    
    def test_get_data_for_visualization_method(self):
        visualization_data = self.service.get_data_for_visualization()
        self.assertIn("bar_chart", visualization_data)
        self.assertIn("bins_histogram", visualization_data)
        self.assertIsInstance(visualization_data["bar_chart"], str)
        self.assertIsInstance(visualization_data["bins_histogram"], str)
        self.__test_image(visualization_data["bar_chart"])
        self.__test_image(visualization_data["bins_histogram"])