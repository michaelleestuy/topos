import urllib3
import sys
from bs4 import BeautifulSoup
import pandas as pd


entries = 50

http = urllib3.PoolManager()
url = 'https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population'
response = http.request('GET', url)


if response.status != 200:
    print('Problem with request, status_code = ', page.status_code, file = sys.stderr, flush = True)
    print("Do not continue.", file = stderr, flush = True)


html = BeautifulSoup(response.data, 'lxml')

#(html.prettify)

my_table = html.find('table', {'class':'wikitable sortable'})

new_table = pd.DataFrame(columns=range(0,12), index=range(0, entries+1))

row_marker = 0
for row in my_table.find_all('tr')[:entries+1]:
    column_marker = 0
    columns = row.find_all('td')
    for column in columns:
        new_table.iat[row_marker, column_marker] = column.get_text()
        column_marker += 1
    row_marker += 1

clean_table = pd.DataFrame(columns=[0,1,2], index=range(0,entries+1))

for i in range(1, entries+1):
    newstring = new_table.iat[i,1]
    if '[' in newstring:
        newstring = newstring[:newstring.find('[')]
    else:
        newstring = newstring[:-1]
    clean_table.iat[i,0] = newstring


    clean_table.iat[i,1] = int(new_table.iat[i, 3][:-1].replace(',', ''))

    clean_table.iat[i,2] = int(new_table.iat[i,4][:-1].replace(',',''))

clean_table.iat[0,0] = 'Cities'
clean_table.iat[0,1] = 'Population(2018)'
clean_table.iat[0,2] = 'Population(2010)'
print(clean_table)