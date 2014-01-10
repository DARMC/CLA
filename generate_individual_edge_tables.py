import unicodecsv as csv
import os

def pair_exists(i):
    """ Check of both required files are in directory """
    nodes = os.path.exists('Nodes/cla_volume_{0:02d}_nodes.csv'.format(i))
    movements = os.path.exists('Movements/cla_volume_{0:02d}_movements.csv'.format(i))
    return True if nodes and movements else False

def find_node_uid(candidate_node, node_database):
    """ Return ID of node corresponding to start or end point of edge """
    return [node[0] for node in node_database if node[1:4] == candidate_node][0]

def load(infile):
    """ Return all rows intact except header"""
    with open(infile,'rU') as inf:
        return [line for line in csv.reader(inf)][1:]

if __name__ == '__main__':
    for x in xrange(1, 12):
        if pair_exists(x):
            # Get input data
            nodefile = 'Nodes/cla_volume_{0:02d}_nodes.csv'.format(x)
            nodes = load(nodefile)
            movementfile = 'Movements/cla_volume_{0:02d}_movements.csv'.format(x)
            segments = load(movementfile)       

            # Create edge table
            edge_table = []
            for i, segment in enumerate(segments):
                # assemble output
                from_node_data = segment[1:4]
                source = find_node_uid(from_node_data, nodes)
                to_node_data = segment[14:17]
                target = find_node_uid(to_node_data, nodes)
                tmp_edge = [source, target] + from_node_data + to_node_data + [segment[26], str(i)]
                # add output to edge table
                edge_table.append(tmp_edge)

            # Write output file
            outfilename = 'cla_volume_{0:02d}_edges.csv'.format(x)
            
            with open('Edges/'+outfilename, 'wb') as outf:
                writer = csv.writer(outf)
                writer.writerow(['Source', 'Target', 'Fr Place1', 'Fr Place2', \
                                 'Fr Place 3', 'To Place1', 'To Place2', \
                                 'To Place 3', 'WKT String', 'Edge UID'])
                writer.writerows(edge_table)
            
            print '>> Generated edge table for CLA {0}'.format(str(x))
        
        else:
            #print 'Required files not found for CLA {0}'.format(str(x))
            pass
            