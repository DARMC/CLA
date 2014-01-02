import os
import sqlite3 as sqlite
import sys
import unicodecsv as csv

def set_up_node_table(c):
    """
    Set up nodes table; no need to drop table if exists because script 
    can only be run if database 'CLA.sqlite' is not already set up in 
    project directory.
    """

    c.execute('''CREATE TABLE IF NOT EXISTS nodes ([id] INTEGER, 
        [Library or Archive] TEXT, [City or Region] TEXT, [Country] TEXT,
        [Centroid Type] TEXT, [Latitude] REAL, [Longitude] REAL, 
        [WKT String] TEXT)''')

def populate_node_table(c, conn, nodes_file):
    """
    Insert contents of CSV file into nodes table
    """
    with open(nodes_file, 'rU') as inf:
        nodes = [row for row in csv.reader(inf)][1:]
    for n in nodes:
        n[0], n[5], n[6] = int(n[0]), float(n[5]), float(n[6])

    c.executemany('''INSERT INTO nodes VALUES (?,?,?,?,?,?,?,?)''', nodes)
    conn.commit()

def set_up_edge_table(c):
    """
    Set up edge table; no need to drop table if exists because script 
    can only be run if database 'CLA.sqlite' is not already set up in 
    project directory.
    """
    c.execute('''CREATE TABLE IF NOT EXISTS edges ([source] INTEGER, 
        [target] INTEGER, [From Library or Archive] TEXT, [From City] TEXT, 
        [From Country] TEXT, [To Library or Archive] TEXT, [To City] TEXT, 
        [To Country] TEXT, [Edge ID] INTEGER)''')

def populate_edge_table(c, conn, edge_file):
    """
    Insert contents of CSV file into edges table
    """
    with open(edge_file, 'rU') as inf:
        edges = [row for row in csv.reader(inf)][1:]
    # convert types as necesscary
    #for e in edges:
    #    e[0], e[1], e[8] = int(e[0]), int(e[1]), int(e[8])

    c.executemany('''INSERT INTO edges VALUES (?,?,?,?,?,?,?,?,?)''', edges)
    conn.commit()

if __name__ == '__main__':
    # don't overwrite existing versions of the database
    if os.path.isfile('cla.sqlite'):
        sys.exit('''>> Database is already set up. \n>> Delete or rename an old 
                    version if you want to rewrite it.''')
    
    # create database and connect to it
    conn = sqlite.connect('cla.sqlite')
    c = conn.cursor()
    
    # set up nodes
    set_up_node_table(c)
    populate_node_table(c, conn, 'Nodes/all_nodes.csv')
    
    # set up edges
    set_up_edge_table(c)
    populate_edge_table(c, conn, 'Edges/all_edges.csv')
