# Pokeberries Statistics API

Simple API developed in Django that retrieves data related to pokeberries and performs statistical calculations on them, using the [Poke API](https://pokeapi.co/docs/v2#berries).

The API consists of one simple endpoint **/allBerryStats**.

## allBerryStats
This endpoint fetches data from the Poke API, specifically the [berries endpoint](https://pokeapi.co/docs/v2#berries-section), and performs statistical calculations with the **growth_time** property. As the Poke API documentation states, the **growth time** is:
> Time it takes the tree to grow one stage, in hours. Berry trees go through four of these growth stages before they can be picked.

The response looks like this:

```json
{
    "berries_names": [
        "cheri",
        "chesto",
        "pecha",
        ...
    ],
    "min_growth_time": 2,
    "median_growth_time": 15.0,
    "max_growth_time": 24,
    "variance_growth_time": 62.47,
    "mean_growth_time": 12.86,
    "frequency_growth_time": {
        "3": 5,
        "4": 3,
        "12": 1,
        ...
    }
}
```

* **berries_names** is a list containing all the names of the pokeberries retrieved.
* **min_growth_time** is an integer with the minium growth time among all retrieved pokeberries.
* **median_growth_time** is a float with the median of the growth time for all retrieved pokeberries.
* **max_growth_time** is an integer with the maxium growth time among all retrieved pokeberries.
* **variance_growth_time** is a float with the variance of the growth time for all retrieved pokeberries.
* **mean_growth_time** is a float with the mean of the growth time for all retrieved pokeberries.
* **frequency_growth_time** is a dict containing the number of times each growh time appears among all the pokeberries.

# 
