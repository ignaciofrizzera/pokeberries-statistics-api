from collections import Counter
from typing import List, Dict, Any
import statistics
import math
import requests

class BerriesService:
    
    __base_url = "https://pokeapi.co/api/v2/berry"

    @staticmethod
    def __get_growth_time_median(growth_times: List[int]) -> float:
        return round(float(statistics.median(growth_times)), 2)

    @staticmethod
    def __get_growth_time_variance(growth_times: List[int]) -> float:
        return round(float(statistics.variance(growth_times)), 2)

    @staticmethod
    def __get_growth_time_mean(growth_times: List[int]) -> float:
        return round(float(statistics.mean(growth_times)), 2)
    
    @staticmethod
    def __get_growth_time_frequency(growth_times: List[int]) -> Counter:
        return Counter(growth_times)

    def get_statistics(self) -> Dict[str, Any]:
        response = requests.get(self.__base_url).json()
        berries: List[Dict[str, str]] = response.get('results')

        while next_request:= response.get('next'):
            response = requests.get(next_request).json()
            berries.extend(response.get('results'))

        berries_names = []
        min_growth_time = math.inf
        max_growth_time = -1
        growth_times = []
        # 64 berries -> 64 requests -> ~17s probably can be optimized
        for berry in berries:
            berry_data: Dict[str, Any] = requests.get(berry.get('url')).json()
            # name
            berries_names.append(berry_data.get('name'))
            # growth_time
            growth_time = berry_data.get('growth_time')
            growth_times.append(growth_time)
            # min/max growth_time
            if growth_time > max_growth_time:
                max_growth_time = growth_time
            if growth_time < min_growth_time:
                min_growth_time = growth_time

        return {
            "berries_names": berries_names,
            "min_growth_time": min_growth_time,
            "median_growth_time": self.__get_growth_time_median(growth_times),
            "max_growth_time": max_growth_time,
            "variance_growth_time": self.__get_growth_time_variance(growth_times),
            "mean_growth_time": self.__get_growth_time_mean(growth_times),
            "frequency_growth_time": self.__get_growth_time_frequency(growth_times)
        }