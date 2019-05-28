#Wikipedia Scraper for Topos 2019

######Michael Lee
######Data Engineering Internship Assignment

The goal of this project was to capture and clean data about some of the largest cities in the United States from unconventional datasets, such as Wikipedia. To do so, this Python3 takes in html and converts it to a CSV for the data we want. The main source of data is [this Wikipedia page](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population), which also provides links to individual city pages where more data can be scraped.

###Prerequisites

- pandas
- urllib3
- bs4

###Usage

The main function:
```
MyScraper.main_scraper(fields, size, outf):
    """
    :param fields: List[str], data we want
    :param size: int, number of cities we want data for
    :param outf: str, name of csv file to put data into
    :return: None
    """
```

####Optimized Fields

This data is gathered directly from [the main list of cities](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population), and thusly, is guaranteed to be consistent amongst all of the cities.

- `'Rank'`: numeral ranking of the city based on population.
- `'City'`: name of of the city
- `'State'`: state that the city is located in
- `'Population (2018)'`
- `'Population (2010)'`
- `'Change'`: percent change of population from 2010 -> 2018
- `'2016 Land Area (sq mi)'` and `'2016 Land Area (km2)'`
- `'2016 Population Density (/sq mi)'` and `'2016 Population Density (/km2)'`'
- `'Location'`: Longitude and Latitude data

####Other Fields

Other data may still be gathered using `MyScraper.main_scraper()`, but the consistency of that data may vary depending on its availability on individual city Wikipedia pages. (ex. not all cities have a date of settlement, or a listed City Attorney.) Any data listed on the infobox of a city's Wikipedia page can be collected by the scraper. If a city is missing a datapoint for a certain field, it will be left blank on the CSV. Examples of some additional fields:

- `'Mayor'`: name of the mayor and their political party
- `'Elevation'`: geographic elevation
- `'Time zone'`
- `'Website'`: official city website

####Size

The number of cities we want data for; the scraper will collect data on this number of cities, going from largest to smallest from [the main list of cities](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population).

####Sample Code

This code can be found in `RunScraper.py`:

```buildoutcfg
import MyScraper

MyScraper.main_scraper(['City', 'Country', 'State', 'Population (2018)', 'Population (2010)', '2016 Land Area (sq mi)',
                        'Type', 'Body', 'Mayor', 'Time zone', ],
                       200,
                       'data.csv')
```

This will generate a CSV file `data.csv` with headers that looks like this:

```buildoutcfg
City,Country,State,Population (2018),Population (2010),2016 Land Area (sq mi),Type,Body,Mayor,Time zone
New York City, United States, New York,8398748,8175133,301.5 sq mi,Mayor–Council,New York City Council,Bill de Blasio (D),UTC−05:00 (EST)
Los Angeles, United States, California,3990456,3792621,468.7 sq mi,Mayor-Council-Commission,Los Angeles City Council,Eric Garcetti (D),UTC−08:00 (Pacific)
Chicago, United States, Illinois,2705994,2695598,227.3 sq mi,Mayor–council,Chicago City Council,Lori Lightfoot (D),UTC−06:00 (Central)
... (followed by 197 more lines)
```

####Other Uses/Future Improvements

```buildoutcfg
MyScraper.scrape_page(end, fields):
    """
    :param end: str, URL of page (ex. '/wiki/New_York_City')
    :param fields: List[str], data we want
    :return: DataFrame, contains data we want
    """
```
- The `MyScraper.scrape_page()` function is already called by `MyScraper.main_scraper()` above, but it can also be used to collect data from the infobox on any Wikipedia page.

- With a few tweaks, `MyScraper.main_scraper()` can be used to collect data from any branching Wikipedia table. 

####Bugs and Issues
