import unicodecsv as csv
import os

def pair_exists(nodefile, movement_file):
    """
    Check of both required files are in directory
    """
    nodes = os.path.exists(nodefile)
    movements = os.path.exists(movement_file)
    return True if nodes and movements else False

def load(infile):
    """
    Return all rows intact except header
    """
    with open(infile,'rU') as inf:
        return [line for line in csv.reader(inf)][1:]

def find_node_uid(candidate_node, node_database):
    """
    Return ID of node corresponding to start or end point of edge
    """
    return [node[0] for node in node_database if node[1:4] == candidate_node][0]

if __name__ == '__main__':
    movementfile = 'Complete CLA Database_movements.csv'
    nodefile = 'Complete CLA Database Points.csv'
    if pair_exists(nodefile, movementfile):
        print '>> Generating Edge Table...',
        nodes = load(nodefile)
        segments = load(movementfile)       

        # Create edge table
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
        
    else:
        print 'Required files not found'
        pass
            