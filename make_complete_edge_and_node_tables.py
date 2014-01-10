import glob
import os
import unicodecsv as csv
import xlwt

def import_file(infile, mode = False):
    """
    Return data from edge and node csv files as a list.
    """
    with open(infile, 'r') as inf:
        if mode == 'Node':
            return [line[1:] for line in csv.reader(inf)][1:]
        elif mode == 'Edge':
            return[line[2:8] for line in csv.reader(inf)][1:]

def remove_duplicate_nodes(nodes):
    """
    Preserve only unique rows. 
    """
    immutable_nodes = [tuple(node) for node in nodes]
    nodeset = set(immutable_nodes)
    nodelist = [list(node) for node in nodeset]
    return nodelist

def find_node_id(place, node_table):
    """
    Return the ID of the node that matches <place>. If more than one matching 
    node existsm, it will return the first one, but this indicates a larger 
    problem with the implementation and should not occur in practice.
    """
    for row in node_table:
        if row[1:4] == place:
            return [row[0]]

if __name__ == '__main__':
    # Import nodes from all files
    node_files = glob.glob(os.path.join('Nodes/cla_volume_[0-1][0-9]_nodes.csv'))
    print '\n>> Importing nodes from {0} files...'.format(len(node_files)),
    all_nodes = []
    for n in node_files:
        all_nodes += import_file(n, mode='Node')

    # Create table of unique nodes
    unique_nodes = remove_duplicate_nodes(all_nodes)
    print 'Got {0} unique nodes'.format(len(unique_nodes))
    for idx, node in enumerate(unique_nodes):
        node.insert(0, str(idx))

    # Import edges
    edge_files = glob.glob(os.path.join('Edges/cla_volume_[0-1][0-9]_edges.csv'))
    print '>> Importing edges from {0} files...'.format(len(edge_files)),
    all_edges = []
    for e in edge_files:
        all_edges += import_file(e, mode='Edge')
    print 'Got {0} edges'.format(len(all_edges))

    # Add node numbers to edge tables in Gephi format
    print '>> Matching Edge and Node Tables'
    final_edges = []
    for idx, line in enumerate(all_edges):
        line.append(str(idx))
        to_node = find_node_id(line[0:3], unique_nodes)
        fr_node = find_node_id(line[3:6], unique_nodes)
        output = to_node + fr_node + line
        final_edges.append(output)

    # Write out node table
    print '>> Writing Complete Node Table'
    with open('Nodes/all_nodes.csv','w') as outf:
        writer = csv.writer(outf)
        header = ['ID', 'Library or Archive', 'City or Region', \
            'Country','Centroid','Latitude','Longitude','WKT String']
        unique_nodes.insert(0, header)
        writer.writerows(unique_nodes)

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('nodes')
    for i, row in enumerate(unique_nodes):
        for j, field in enumerate(row):
            sheet.write(i, j, field.encode('utf-8'))

    # Write out edge table
    print '>> Writing Complete Edge Table\n'
    with open('Edges/all_edges.csv','w') as outf:
        writer = csv.writer(outf)
        edge_header = ['Source', 'Target', 'Fr Place1', 'Fr Place2', \
            'Fr Place 3','To Place1','To Place2','To Place 3','Edge UID']
        final_edges.insert(0, edge_header)
        writer.writerows(final_edges)
    
    sheet2 = book.add_sheet('edges')
    for i, row in enumerate(final_edges):
        for j, field in enumerate(row):
            sheet2.write(i, j, field.encode('utf-8'))

    book.save('edges_and_nodes.xls')