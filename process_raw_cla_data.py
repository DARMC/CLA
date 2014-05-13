import subprocess
from time import time

if __name__ == '__main__':
	start = time()
	subprocess.call('python generate_cla_database_segments.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)
	subprocess.call('python generate_edge_table.py', shell = True)
	print 'Runtime: {0:.3f} seconds'.format(time() - start)