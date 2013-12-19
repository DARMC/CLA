import unicodecsv as ucsv
import sys
import glob
import os
import time

def find_node_uid(candidate_node, node_database):
	for node in node_database:
		if node[1:4] == candidate_node:
			return node[0]
	return ''

def pair_exists(i):
	if os.path.exists('cla_volume_{0}_nodes.csv'.format(str(i))) and \
	   os.path.exists('cla_volume_{0}_movements.csv'.format(str(i))):
	    return True
	else:
		return False

for x in xrange(1,12):
	if pair_exists(x):
		nodefile = 'cla_volume_{0}_nodes.csv'.format(str(x))
		movementfile = 'cla_volume_{0}_movements.csv'.format(str(x))
		with open(nodefile,'rU') as inf:
			nodes = [line for line in ucsv.reader(inf)]

		with open(movementfile,'rU') as inf2:
			segments = [line for line in ucsv.reader(inf2)][1:]


		i = 0
		final_edges = []
		final_edges.append(['Source','Target','Fr Place1','Fr Place2','Fr Place 3','To Place1','To Place2','To Place 3','Edge UID'])
		for segment in segments:
			tmp_edge = []
			edge_uid = [str(i)]
			from_node_data = segment[1:4]
			source = [find_node_uid(from_node_data, nodes)]
			to_node_data = segment[14:17]
			target = [find_node_uid(to_node_data, nodes)]
			tmp_edge += source
			tmp_edge += target
			tmp_edge += from_node_data
			tmp_edge += to_node_data
			tmp_edge += edge_uid
			i += 1
			final_edges.append(tmp_edge)

		outfilename = 'cla_volume_{0}_edges.csv'.format(str(x))
		with open(outfilename, 'wb') as outf:
			writer = ucsv.writer(outf)
			writer.writerows(final_edges)
		print 'Generated edge table for CLA {0}'.format(str(x))
	else:
		print 'Required files not found to generate edge table for CLA {0}'.format(str(x))
