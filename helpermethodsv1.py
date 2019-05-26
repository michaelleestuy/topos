import urllib3
import sys
from bs4 import BeautifulSoup
import pandas as pd



def scrape_page(end, fields):
    http = urllib3.PoolManager()
    url = 'https://en.wikipedia.org' + end
    response = http.request('GET', url)

    if response.status != 200:
        print('Problem with request, status_code = ', page.status_code, file=sys.stderr, flush=True)
        print("Do not continue.", file=stderr, flush=True)

    html = BeautifulSoup(response.data, 'lxml')


    my_info = html.find('table', {'class': 'infobox geography vcard'})

    grab_data = pd.DataFrame(columns=[0,1], index=range(100))

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




    output_data = pd.DataFrame(columns=[0], index=range(len(fields)))

    print(grab_data)
    #print(output_data)
    #print(grab_data.iat[9,0])

    #print(grab_data.iat[0,1])

    start_point = 0
    while grab_data.iat[start_point,1] == grab_data.iat[0,1]:
        start_point += 1

    #print(start_point)

    for j in range(len(fields)):
        for i in range(start_point,50):

            if type(grab_data.iat[i,0]) != type(0.0) and fields[j] in grab_data.iat[i,0]:
                #print('Found: ', fields[j], 'At: ', str(i) + ',' + '1', grab_data.iat[i,1])

                output_data.iat[j,0] = grab_data.iat[i,1]


                break

    return output_data

print(scrape_page('/wiki/Chicago', [  'Country', 'State', 'Mayor', 'lmao']))