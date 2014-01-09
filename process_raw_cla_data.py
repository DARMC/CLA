import subprocess

if __name__ == '__main__':
	subprocess.call('python generate_cla_database_segments.py', shell = True)
	subprocess.call('python generate_individual_edge_tables.py', shell = True)
	subprocess.call('python make_complete_edge_and_node_tables.py', shell = True)
	# subprocess.call('python set_up_sqlite_database.py')