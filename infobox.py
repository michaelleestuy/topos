import urllib3
import sys
from bs4 import BeautifulSoup
import pandas as pd
import wptools

http = urllib3.PoolManager()
url = 'https://en.wikipedia.org/wiki/New_york_city'
response = http.request('GET', url)


if response.status != 200:
    print('Problem with request, status_code = ', page.status_code, file = sys.stderr, flush = True)
    print("Do not continue.", file = stderr, flush = True)


html = BeautifulSoup(response.data, 'lxml')

my_title = html.find('h1').get_text()



my_info = html.find('table', {'class':'infobox geography vcard'})


output_table = pd.DataFrame(columns=[0,1], index=range(50))

row_marker = 0
for row in my_info.find_all('tr'):
    column_marker = 0
    columns = row.find_all(['td','th'])
    for column in columns:
        output_table.iat[row_marker, column_marker] = column.get_text()
        column_marker += 1
    row_marker += 1

clean_table = pd.DataFrame(columns=[0,1], index=range(50))

print(output_table)