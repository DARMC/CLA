try:
	import unicodecsv as csv
except ImportError:
	print 'Could not load unicodecsv module. Loading standard csv library instead\n'
	import csv

def condense(list):
	unique_rows = []
	found_pairs = []
	for row in list:
		if row[1:3] not in found_pairs:
			found_pairs.append(row[1:3])
			unique_rows.append(row)
	return unique_rows

if __name__ == '__main__':
	with open('Nodes/all_nodes.csv', 'r') as inf:
		data = [[row[0]] + row[2:] for row in csv.reader(inf)]


	with open('Nodes/all_city_level_nodes.csv','w') as outf:
		writer = csv.writer(outf)
		print len(data)-1
		writer.writerows(condense(data))
