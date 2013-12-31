MAKE_NODE_TABLE = '''
	CREATE TABLE IF NOT EXISTS nodes (
		[Node ID] INTEGER,
		[Library or Archive] TEXT,
		[City or Region] TEXT,
		[Country] TEXT,
		[Centroid Type] TEXT,
		[Latitude] REAL,
		[Longitude] REAL,
		[WKT String] TEXT
	)
	'''

MAKE_EDGE_TABLE = ''' * '''

