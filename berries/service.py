from collections import Counter
from typing import List, Dict, Any
import statistics
import requests

class BerriesService:
    
    __base_url = "https://pokeapi.co/api/v2/berry"
    def __init__(self):
        self.__base_url = "https://pokeapi.co/api/v2/berry"
        self.__session = requests.Session()

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

    def __get_all_berries(self) -> List[Dict[str, str]]:
        response = self.__session.get(self.__base_url).json()
        berries: List[Dict[str, str]] = response.get('results')

        while next_request:= response.get('next'):
            response = self.__session.get(next_request).json()
            berries.extend(response.get('results'))
        
        return berries
    
    def get_statistics(self) -> Dict[str, Any]:
        berries_names = []
        growth_times = []
        for berry in self.__get_all_berries():
            berry_data: Dict[str, Any] = self.__session.get(berry.get('url')).json()
            berries_names.append(berry_data.get('name'))
            growth_times.append(berry_data.get('growth_time'))

        return {
            "berries_names": berries_names,
            "min_growth_time": min(growth_times),
            "median_growth_time": self.__get_growth_time_median(growth_times),
            "max_growth_time": max(growth_times),
            "variance_growth_time": self.__get_growth_time_variance(growth_times),
            "mean_growth_time": self.__get_growth_time_mean(growth_times),
            "frequency_growth_time": self.__get_growth_time_frequency(growth_times)
        }