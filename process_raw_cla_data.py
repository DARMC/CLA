import subprocess
from time import time

if __name__ == '__main__':
	start = time()
	subprocess.call('python generate_cla_database_segments.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	subprocess.call('python generate_individual_edge_tables.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	subprocess.call('python make_complete_edge_and_node_tables.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	subprocess.call('python create_master_spreadsheet.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	subprocess.call('python condense_node_table.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	# subprocess.call('python set_up_sqlite_database.py')