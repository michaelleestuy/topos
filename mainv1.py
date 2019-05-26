import urllib3
import sys
from bs4 import BeautifulSoup
import pandas as pd
import wptools

entries = 5

http = urllib3.PoolManager()
url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
response = http.request('GET', url)


if response.status != 200:
    print('Problem with request, status_code = ', page.status_code, file = sys.stderr, flush = True)
    print("Do not continue.", file = stderr, flush = True)


html = BeautifulSoup(response.data, 'lxml')

my_table = html.find('table', {'class':'wikitable sortable'})

new_table = pd.DataFrame(columns=range(11), index=range(entries+1))

row_marker = 0
for row in my_table.find_all('tr')[:entries+1]:
    columns = row.find_all('td')

    if row_marker == 0:
        row_marker += 1
        continue

    city_name = columns[1].get_text()
    if '[' in city_name:
        city_name = city_name[:city_name.find('[')]
    else:
        city_name = city_name[:-1]

    new_table.iat[row_marker,0] = city_name

    #print(city_name)

    new_table.iat[row_marker,1] = columns[1].find('a', href=True).get('href')

    row_marker += 1
'''
for i in range(1, entries+1):
    http = urllib3.PoolManager()
    url = 'https://en.wikipedia.org' + new_table.iat[i,1]
    response = http.request('GET', url)

    if response.status != 200:
        print('Problem with request, status_code = ', page.status_code, file=sys.stderr, flush=True)
        print("Do not continue.", file=stderr, flush=True)

    html = BeautifulSoup(response.data, 'lxml')
'''






print(new_table)