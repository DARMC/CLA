import os
import sqlite3 as sqlite
import sys
import unicodecsv as csv
import glob

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

    c.executemany('''INSERT INTO edges VALUES (?,?,?,?,?,?,?,?,?)''', edges)
    conn.commit()

def set_up_attributes_table(c):
    """
    Set up attributes table for CLA manuscripts; no need to drop table 
    if exists because script can only be run if database 'CLA.sqlite' 
    is not already set up in project directory.
    """
    c.execute('''CREATE TABLE IF NOT EXISTS attributes (MSID REAL, CLA REAL, 
        [CLA-alt] REAL, Library TEXT, City TEXT, Country TEXT, librarylat REAL,
        librarylong REAL, [order-libr] REAL, Fonds TEXT, Signature TEXT, 
        Folios TEXT, [folios-no] TEXT, Script TEXT, startdate TEXT, 
        enddate TEXT, Author TEXT, Work TEXT, folioL TEXT, folioW TEXT, 
        [folio-q] TEXT, wsL TEXT, wsW TEXT, wsQ TEXT, Lines TEXT, Columns TEXT, 
        [Ruling 1] TEXT, [Ruling 2] TEXT, wherecopied TEXT, wherecopied2 TEXT, 
        wherecopied3 TEXT, [where-q] TEXT, [where-centroid] TEXT, 
        wherecopiedlat REAL, wherecopiedlong REAL, wherecopiedalt TEXT, 
        wherecopiedalt2 TEXT,[wherealt-centroid] TEXT, wherealtlat REAL, 
        wherealtlong REAL, rel TEXT, [order-copied] TEXT, comments TEXT, 
        [emphasis scripts] TEXT, ornamtation TEXT, images TEXT, 
        [palaeographical links] TEXT, [to do] TEXT)''')

def populate_attribute_table(c, conn):
    for filename in glob.glob('cla_volume_[0-1][0-9].csv'):
        with open(filename, 'rU') as inf:
            rows = [row[0:48] for row in csv.reader(inf)][1:]
            
            c.executemany('''INSERT INTO attributes VALUES (?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?)''', rows)
            conn.commit()


if __name__ == '__main__':
    # don't overwrite existing versions of the database
    if os.path.isfile('cla.sqlite'):
        os.remove('cla.sqlite')
        #sys.exit('''>> Database is already set up. \n>> Delete or rename an old 
                    #version if you want to rewrite it.''')
    
    # create database and connect to it
    conn = sqlite.connect('cla.sqlite')
    c = conn.cursor()
    
    # set up nodes
    print '>> Creating edge and node tables'
    set_up_node_table(c)
    populate_node_table(c, conn, 'Nodes/all_nodes.csv')
    
    # set up edges
    set_up_edge_table(c)
    populate_edge_table(c, conn, 'Edges/all_edges.csv')

    # set up MS attribute table
    print '>> Creating manuscript attributes table'
    set_up_attributes_table(c)
    populate_attribute_table(c, conn)
