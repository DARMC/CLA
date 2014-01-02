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

INSERT_LINE_INTO_NODE_TABLE = '''
	INSERT INTO nodes (
		[Node ID],
		[Library or Archive],
		[City or Region],
		[Country],
		[Centroid Type],
		[Latitude],
		[Longitude],
		[WKT String]
	)
	VALUES (
		?, ?, ?, ?, ?, ?, ?, ?
	)
	'''

MAKE_EDGE_TABLE = '''
	CREATE TABLE IF NOT EXISTS edges ( 
		[From Node ID] INTEGER, 
		[To Node ID] INTEGER, 
		[From Library or Archive] TEXT, 
		[From City] TEXT, 
		[From Country] TEXT, 
		[To Library or Archive] TEXT, 
		[To City] TEXT, 
		[To Country] TEXT, 
		[Edge ID] INTEGER
	) 
	'''

MAKE_ATTRIBUTE_TABLE = '''
	CREATE TABLE IF NOT EXISTS attributes (
	)
	'''

MAKE_COMPLETE_TABLE = '''
	CREATE TABLE IF NOT EXISTS complete (
	)
	'''

