from typing import List, Dict, Any, Union, Tuple
from collections import Counter
import matplotlib
matplotlib.use('Agg')
from matplotlib.axes import Axes
import matplotlib.pyplot as plt
import io
import base64
import statistics
import requests

class BerriesService:
    
    def __init__(self):
        self.__base_url = "https://pokeapi.co/api/v2/berry"
        self.__session = requests.Session()

    @staticmethod
    def __get_growth_time_median(growth_times: List[int]) -> float:
        return round(float(statistics.median(growth_times)), 2)

    @staticmethod
    def __get_growth_time_variance(growth_times: List[int]) -> float:
        if len(growth_times) == 1:
            return 0.0
        return round(float(statistics.variance(growth_times)), 2)

    @staticmethod
    def __get_growth_time_mean(growth_times: List[int]) -> float:
        return round(float(statistics.mean(growth_times)), 2)
    
    @staticmethod
    def __get_growth_time_frequency(growth_times: List[int]) -> int:
        return statistics.mode(growth_times)

    def __get_all_berries(self) -> List[Dict[str, str]]:
        response = self.__session.get(self.__base_url).json()
        berries: List[Dict[str, str]] = response.get('results')

        while next_request:= response.get('next'):
            response = self.__session.get(next_request).json()
            berries.extend(response.get('results'))
        
        return berries
    
    def get_statistics(self, for_visualization: bool = False) -> Union[Dict[str, Any], Tuple[Dict[str, Any], List[int]]]:
        berries_names = []
        growth_times = []
        for berry in self.__get_all_berries():
            berry_data: Dict[str, Any] = self.__session.get(berry.get('url')).json()
            berries_names.append(berry_data.get('name'))
            growth_times.append(berry_data.get('growth_time'))

        statistics_data = {
            "berries_names": berries_names,
            "min_growth_time": min(growth_times),
            "median_growth_time": self.__get_growth_time_median(growth_times),
            "max_growth_time": max(growth_times),
            "variance_growth_time": self.__get_growth_time_variance(growth_times),
            "mean_growth_time": self.__get_growth_time_mean(growth_times),
            "frequency_growth_time": self.__get_growth_time_frequency(growth_times)
        }

        if not for_visualization:
            return statistics_data
        
        return statistics_data, growth_times
    
    @staticmethod
    def __encode_plot() -> str:
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        return base64.b64encode(image_png).decode('utf-8')
    
    @staticmethod
    def __setup_plot(title: str, x_label: str, y_label: str) -> Axes:
        _, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        return ax
    
    def __generate_bar_chart_image(self, labels: List[Any], values: List[Any], title: str, x_label: str, y_label: str) -> str:
        ax = self.__setup_plot(title, x_label, y_label)
        ax.set_xticks(labels)
        ax.set_yticks(range(0, max(values) + 1))
        ax.bar(labels, values)
        return self.__encode_plot()
        
    def __generate_bins_histogram_image(self, values: List[int], bins: int, title: str, x_label: str, y_label: str) -> str:
        ax = self.__setup_plot(title, x_label, y_label)
        ax.hist(values, bins=bins, rwidth=0.8)
        return self.__encode_plot()
    
    def get_data_for_visualization(self) -> Dict[str, Any]:
        statistics_data, growth_times = self.get_statistics(for_visualization=True)
        growth_times_counter = Counter(growth_times)
        labels, values= zip(*growth_times_counter.items())

        bar_chart_image = self.__generate_bar_chart_image(
            labels, values, title="Growth Times among the Berries", x_label="Growth Time", y_label="Frequency")
        
        bins_histogram_image = self.__generate_bins_histogram_image(
            growth_times, bins=5, title="Bins of Growth Times", x_label="Bins", y_label="Growth Time")

        statistics_data["bar_chart"] = bar_chart_image
        statistics_data["bins_histogram"] = bins_histogram_image
        
        return statistics_data