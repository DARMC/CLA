import sqlite3 as sqlite
import os
import sys
import syntax

def set_up_node_table(c):
    """
    Set up nodes table and populate it with the contents of the file
    'all_nodes.csv' which should be a complete set of cla nodes.
    """
    c.execute(syntax.MAKE_NODE_TABLE)
    # populate node table

    ##
    # TODO
    ##

def set_up_edge_table(c):
    c.execute(syntax.MAKE_EDGE_TABLE)
    ##
    # TODO
    ##

def set_up_attribute_table(c):
    c.execute(syntax.MAKE_MS_ATTRIBUTE_TABLE)
    ##
    # TODO
    ##

def set_up_complete_table(c):
    c.execute(syntax.MAKE_COMPLETE_TABLE)
    ##
    # TODO
    ##

if __name__ == '__main__':
    #
    if os.path.isfile('cla.db'):
        sys.exit('>> Database is already set up. \n>> Delete or rename an old version if you want to rewrite it.')

    conn = sqlite.connect('cla.db')
    c = conn.cursor()
    set_up_node_table(c)
