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
        """
        Fetches all berry data from the PokeAPI by iterating through paginated results.

        This function makes a GET request to the "https://pokeapi.co/api/v2/berry" endpoint 
        to retrieve a list of berries. Each request contains a portion of the results 
        with a 'next' field pointing to the next page, if available. The function 
        continues making requests until all pages are retrieved.

        Returns: A list of dictionaries, where each dictionary contains a 'name' and 'url' field for each berry.
        
        Example return format:
        [
            {"name": "cheri", "url": "https://pokeapi.co/api/v2/berry/1/"},
            {"name": "chesto", "url": "https://pokeapi.co/api/v2/berry/2/"},
            ...
        ]
        """
        response = self.__session.get(self.__base_url).json()
        berries: List[Dict[str, str]] = response.get('results')

        while next_request:= response.get('next'):
            response = self.__session.get(next_request).json()
            berries.extend(response.get('results'))
        
        return berries
    
    def get_statistics(self, for_visualization: bool = False) -> Union[Dict[str, Any], Tuple[Dict[str, Any], List[int]]]:
        """
        Retrieves statistics about berries growth times from the PokeAPI.

        This function fetches all berries from the PokeAPI, then retrieves the 
        detailed data for each berry, specifically focusing on their growth times. 
        It calculates various statistical metrics such as the minimum, median, 
        maximum, variance, mean, and the most frequent growth time.

        If `for_visualization` is set to True, the function also returns the list 
        of growth times used for statistical calculations. Otherwise, only the 
        statistics are returned.

        Args:
            for_visualization (bool, optional): Flag to include the list of growth 
            times in the return value. Defaults to False.

        Returns:
            Union[Dict[str, Any], Tuple[Dict[str, Any], List[int]]]: 
                - If `for_visualization` is False, returns a dictionary containing 
                the following statistical data:
                - "berries_names" (List[str]): List of berry names.
                - "min_growth_time" (int): Minimum growth time.
                - "median_growth_time" (float): Median of the growth times.
                - "max_growth_time" (int): Maximum growth time.
                - "variance_growth_time" (float): Variance of the growth times.
                - "mean_growth_time" (float): Mean growth time.
                - "frequency_growth_time" (int): Most frequent growth time.
                - If `for_visualization` is True, returns a tuple where the first 
                element is the statistics dictionary (same as above) and the second 
                element is the list of all growth times (List[int]).
        """
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
        """
        Prepares and returns berry growth statistics along with visualization data.

        This method first retrieves berry growth statistics and their corresponding 
        growth times by calling `get_statistics(for_visualization=True)`. It then 
        creates two visualizations: 
        1. A bar chart showing the frequency of each growth time.
        2. A histogram dividing the growth times into bins.

        The generated images for both charts are included in the returned dictionary 
        as encoded strings.

        Returns:
            Dict[str, Any]: A dictionary containing the same statistical data returned by `get_statistics` along with 
            the following visualizations:
            - "bar_chart" (str): Base64-encoded image of the bar chart showing 
            growth time frequencies.
            - "bins_histogram" (str): Base64-encoded image of the histogram dividing 
            growth times into bins.
        """
        statistics_data, growth_times = self.get_statistics(for_visualization=True)
        growth_times_counter = Counter(growth_times)
        labels, values= zip(*growth_times_counter.items())

        bar_chart_image = self.__generate_bar_chart_image(
            labels, values, title="Growth Times among the Berries", x_label="Growth Time", y_label="Frequency")
        
        bins_histogram_image = self.__generate_bins_histogram_image(
            growth_times, bins=5, title="Bins of Growth Times", x_label="Growth Time Bins", y_label="Number of Berries")

        statistics_data["bar_chart"] = bar_chart_image
        statistics_data["bins_histogram"] = bins_histogram_image
        
        return statistics_data