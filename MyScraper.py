import sys
import pandas as pd
import urllib3
from bs4 import BeautifulSoup


# scrape_page is used to extract info from the infobox on individual city wikipages
def scrape_page(end, fields):
    """
    :param end: str, URL of page
    :param fields: List[str], data we want
    :return: DataFrame, contains data we want
    """

    # url processing
    http = urllib3.PoolManager()
    url = 'https://en.wikipedia.org' + end
    response = http.request('GET', url)

    if response.status != 200:
        print('Problem with request, status_code = ', page.status_code, file=sys.stderr, flush=True)
        print("Do not continue.", file=sys.stderr, flush=True)

    html = BeautifulSoup(response.data, 'lxml')

    my_info = html.find('table', {'class': 'infobox geography vcard'})  # html for the table we will parse

    grab_data = pd.DataFrame(columns=[0, 1], index=range(100))  # storage for raw data from the table

    # scraping raw data
    row_marker = 0
    passed = False
    for row in my_info.find_all('tr'):
        column_marker = 0
        columns = row.find_all(['td', 'th'])
        for column in columns:
            c = column.get_text()
            if c != '' and c[-1] == '\n':
                c = c[:-1]
            grab_data.iat[row_marker, column_marker] = c
            column_marker += 1
            if 'Coordinate' in c:
                passed = True

        if not passed:
            grab_data.iat[row_marker, 1] = -1

        row_marker += 1

    output_data = pd.DataFrame(columns=[0], index=range(len(fields)))  # data to be returned

    # this code is needed to skip through the images at the top of the infobox
    # to make sure we actually get data for the fields we are looking for
    start_point = 0
    while grab_data.iat[start_point, 1] == grab_data.iat[0, 1]:
        start_point += 1

    # cleaning and cutting data into what we want
    for j in range(len(fields)):
        for i in range(start_point, 50):

            if type(grab_data.iat[i, 0]) != type(0.0) and fields[j] in grab_data.iat[i, 0]:
                output_data.iat[j, 0] = grab_data.iat[i, 1]
                break

    return output_data


# main_scraper takes data from /wiki/List_of_United_States_cities_by_population
# finds URLs for individual pages and passes them to scrape_page

def main_scraper(fields, size, outf):
    """
    :param fields: List[str], data we want
    :param size: int, number of cities we want data for
    :param outf: str, name of csv file to put data into
    :return: None
    """

    final_table = pd.DataFrame(columns=range(len(fields)), index=range(size + 1))  # storage for final data

    # placeholder to make sure we do not override data already in the table
    for i in range(len(fields)):
        for j in range(size + 1):
            final_table.iat[j, i] = 'Not Found'

    # headers
    for i in range(len(fields)):
        final_table.iat[0, i] = fields[i]

    # more URL processing
    http = urllib3.PoolManager()
    url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
    response = http.request('GET', url)

    if response.status != 200:
        print('Problem with request, status_code = ', page.status_code, file=sys.stderr, flush=True)
        print("Do not continue.", file=stderr, flush=True)

    html = BeautifulSoup(response.data, 'lxml')

    my_table = html.find('table', {'class': 'wikitable sortable'})  # the main table of cities

    table_a = pd.DataFrame(columns=range(11), index=range(size + 1))  # collection for data from table
    links = []  # and URLs

    row_counter = 1
    for row in my_table.find_all('tr')[1:size + 1]:
        column_counter = 0
        for column in row.find_all('td'):
            c = column.get_text().replace(',', '')
            if '[' in c:
                c = c[:c.find('[')]
            else:
                c = c[:-1]
            table_a.iat[row_counter, column_counter] = c
            if column_counter == 1:
                links.append(column.find('a', href=True).get('href'))

            column_counter += 1
        row_counter += 1

    # headers
    table_a.iat[0, 0] = 'Rank'
    table_a.iat[0, 1] = 'City'
    table_a.iat[0, 2] = 'State'
    table_a.iat[0, 3] = 'Population (2018)'
    table_a.iat[0, 4] = 'Population (2010)'
    table_a.iat[0, 5] = 'Change'
    table_a.iat[0, 6] = '2016 Land Area (sq mi)'
    table_a.iat[0, 7] = '2016 Land Area (km2)'
    table_a.iat[0, 8] = '2016 Population Density (/sq mi)'
    table_a.iat[0, 9] = '2016 Population Density (/km2)'
    table_a.iat[0, 10] = 'Location'

    # cleaning and cutting data from table_a and putting into final_table
    for i in range(len(fields)):
        for j in range(11):
            if fields[i] == table_a.iat[0, j]:
                for k in range(size + 1):
                    final_table.iat[k, i] = table_a.iat[k, j]

    # scraping of individual city pages by URL
    progress = 1
    for i in range(len(links)):
        print('Scraping: ', links[i], ' (', str(progress), '/', str(size), ')')  # progress bar for user
        progress += 1
        output_data = scrape_page(links[i], fields)

        for j in range(len(fields)):
            if final_table.iat[i + 1, j] == 'Not Found':
                c = output_data.iat[j, 0]
                if type(c) == type('') and '[' in c:
                    c = c[:c.find('[')] + c[c.find(']') + 1:]
                final_table.iat[i + 1, j] = c

    final_table.to_csv(path_or_buf=outf, index=False, header=False)  # convert to csv
    print('Done!')
    return

###
