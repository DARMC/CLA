import unicodecsv as csv
import os
import sys
import glob
from time import sleep

def import_all_nodes(infile):
	with open(infile, 'r') as inf:
		return [line[1:] for line in csv.reader(inf)][1:]

def remove_duplicate_nodes(nodes):
	unique_nodes = []
	for n in nodes: 
		if n not in unique_nodes:
			unique_nodes.append(n)
	return unique_nodes

def import_all_edges(infile):
	with open(infile,'r') as inf:
		return[line[2:8] for line in csv.reader(inf)][1:]

def find_node_id(place, node_table):
	for row in node_table:
		if row[1:4] == place:
			return [row[0]]

files = glob.glob(os.path.join('cla_volume_?_nodes.csv'))
all_nodes = []

print '>> Importing nodes from {0} files...'.format(len(files)),
for f in files:
	all_nodes += import_all_nodes(f)

compressed_nodes = remove_duplicate_nodes(all_nodes)
print 'Got {0} unique nodes'.format(len(compressed_nodes))
for idx, node in enumerate(compressed_nodes):
	node.insert(0, str(idx))

print '>> Writing unique nodes to output file...'
with open('all_nodes.csv','w') as outf:
	writer = csv.writer(outf)
	writer.writerow(['ID','Library or Archive','City or Region','Country','Centroid','Latitude','Longitude','WKT String'])
	writer.writerows(compressed_nodes)

edge_files = glob.glob(os.path.join('cla_volume_?_edges.csv'))
all_edges = []
print '>> Importing edges from {0} files...'.format(len(edge_files))
for e in edge_files:
	all_edges += import_all_edges(e)
	print len(all_edges)

print '>> Matching edge and node tables'
final_edges = []
for idx, line in enumerate(all_edges):
	line.append(str(idx))
	to_node = find_node_id(line[0:3], compressed_nodes)
	fr_node = find_node_id(line[3:6], compressed_nodes)
	output = to_node + fr_node + line
	final_edges.append(output)

print '>> Writing final edge table'
with open('all_edges.csv','w') as outf:
	writer = csv.writer(outf)
	writer.writerow(['Source','Target','Fr Place1','Fr Place2','Fr Place 3','To Place1','To Place2','To Place 3','Edge UID'])
	writer.writerows(final_edges)
