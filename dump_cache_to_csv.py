import unicodecsv as csv
import json

with open('cache.json','rU') as inf:
	data = json.read(inf)

print data