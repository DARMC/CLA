import unicodecsv as csv
import os
import sys
import glob

def import_all_nodes(infile):
	with open(infile, 'r') as inf:
		return [line[1:] for line in csv.reader(inf)][1:]

def compress_nodes(nodes):
	unique_nodes = []
	for n in nodes: 
		if n not in unique_nodes:
			unique_nodes.append(n)
	return unique_nodes

files = glob.glob(os.path.join('cla_volume_?_nodes.csv'))
all_nodes = []

for f in files:
	all_nodes += import_all_nodes(f)
	print len(all_nodes)

compressed_nodes = compress_nodes(all_nodes)

for idx, node in enumerate(compressed_nodes):
	node.insert(0, str(idx))

with open('all_nodes.csv','w') as outf:
	writer = csv.writer(outf)
	writer.writerow(['ID','Library or Archive','City or Region','Country','Centroid','Latitude','Longitude','WKT String'])
	writer.writerows(compressed_nodes)
