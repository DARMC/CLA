import unicodecsv as csv
import os

def pair_exists(nodefile, movement_file):
    """
    Check of both required files are in the program directory,
    returning either True or False.

    Parameters
    ----------
    nodes : file containing all unique points from the CLA file.
    movements : file containing all unique movements and movement
        magnitudes from the CLA file.
    """
    nodes = os.path.exists(nodefile)
    movements = os.path.exists(movement_file)
    return True if nodes and movements else False

def load(infile):
    """
    Return all rows from 'infile' intact, stripping the header row.

    Parameters
    ----------
    infile : name of file to import.
    """
    with open(infile,'rU') as inf:
        return [line for line in csv.reader(inf)][1:]

def find_node_uid(candidate_node, node_database):
    """
    Return ID of node corresponding to start or end point of edge.

    Patameters
    ----------
    candidate_node : node to match using an existing list.
    node_database : list of all nodes, either points "from" or points "to"
        against which a candidate can be matched.
    """
    return [node[0] for node in node_database if node[1:4] == candidate_node][0]

def create_edge_table(movementfile, nodefile):
    """
    Write a CSV file containing one row per manuscript movement with
    'Source' and 'Target' columns corresponding to the movement points,
    suitable for direct import into Gephi for visualization.

    Parameters
    ----------
    movementfile : name of a file containing raw data about MS movements 
    nodefile : name of file containing all nodes and unique IDs for nodes.
    """
    print '>> Generating Edge Table...',
    nodes = load(nodefile)
    segments = load(movementfile)       

    edge_table = []

    for i, segment in enumerate(segments):
        # assemble output
        from_node_data = segment[1:4]
        source = find_node_uid(from_node_data, nodes)
        to_node_data = segment[18:21]
        target = find_node_uid(to_node_data, nodes)
        tmp_edge = [source, target] + from_node_data + to_node_data + [segment[-1], str(i)]
        # add output to edge table
        edge_table.append(tmp_edge)


    # Write output file
    outfilename = 'cla_edges.csv'        
    with open(outfilename, 'wb') as outf:
        writer = csv.writer(outf)
        writer.writerow(['Source', 'Target', 'Fr Place1', 'Fr Place2', \
                         'Fr Place 3', 'To Place1', 'To Place2', \
                         'To Place 3', 'WKT String', 'Edge UID'])
        writer.writerows(edge_table)
    
    print 'COMPLETED'

if __name__ == '__main__':
    movementfile = 'Complete CLA Database_movements.csv'
    nodefile = 'Complete CLA Database Points.csv'
    if pair_exists(nodefile, movementfile):
        create_edge_table(movementfile, nodefile)    
    else:
        print 'Required files not found'
            