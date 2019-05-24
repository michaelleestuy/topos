import wptools



so = wptools.page('Atlanta')
so.get_parse()
infobox = so.data['infobox']

#print(infobox)

print(infobox.keys())
#use population_total

if 'population_total' in infobox:
    print('Population: ', infobox['nickname'])
else:
    print('not found')
'''
cities = ['https://en.wikipedia.org/wiki/Los_Angeles']

pages = []

for i in cities:
    pages.append(wptools.page(wiki=i))

for i in pages:
    i.get_parse()

pops = {}

for i in range(len(cities)):
    pops[cities[i]] = pages[i].data['infobox']['population_total']

print(pops)'''