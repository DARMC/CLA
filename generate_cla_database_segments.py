import time
import unicodecsv as ucsv
import sys
import glob
import os

def import_csv(infile):
    """
    Return raw data array from csv file
    """
    return [line for line in ucsv.reader(open(infile,'rU'))]

def import_excel(infile):
    """
    Return raw data arraw from excel file
    """
    import xlrd
    data = []
    workbook = xlrd.open_workbook(infile)
    worksheet = workbook.sheet_by_name('CLA')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    curr_row = -1
    while curr_row < num_rows:
        row_data = []
        curr_row += 1
        row = worksheet.row(curr_row)
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            row_data.append(worksheet.cell_value(curr_row, curr_cell))
        data.append(row_data)
        #print len(row_data)
    return data

def write_unique_points(d, inf_name):
    def is_in(existing, c):
        match = False
        if len(existing) > 0:
            for r in existing:
                if r[0:3] == c[0:3]:
                    match = True
        return match
    
    def make_wkt_point(lng, lat):
        """
        Returns a WKT point for given input strings - no validation
        """
        return ['POINT({0} {1})'.format(lng, lat)]

    with open(os.path.join('Nodes', inf_name+'_nodes.csv'),'w') as outf:
        writer = ucsv.writer(outf)
        writer.writerow(['ID','Library or Archive','City or Region','Country','Centroid','Latitude','Longitude','WKT String'])
        # create WKT geometry
        data_to_write = []
        for row in d:
            print row
            #if len(row) != 13: print row
            if row[8] != '' and row[7] != '':
                rmod = row[1:5] + row[7:9] + make_wkt_point(row[8], row[7])
                
                data_to_write.append(rmod)

        #data_to_write = [row[1:5] + row[7:9] + make_wkt_point(row[8], row[7]) for row in d if row[8] != '' and row[7] != '']
        
        unique_rows = []
        for row in data_to_write:
            if not is_in(unique_rows,row):
                unique_rows.append(row)
        
        for idx, row in enumerate(unique_rows):
            row.insert(0, str(idx))
        
        writer.writerows(unique_rows)  

def denormalize_dataset(raw_data, inf_name):
    """Return one manuscript point per line"""
    # denormalize rows
    denormalized_data = []
    # MSID, Place 1, Place 2, Place 3, Centroid, Certainty, Relation, 
    #Lat, Long, Ord, Comment
    for row in raw_data:
    #place2  place2.1    place2.2    pl2-centr   pl2-q   rel2    declat2 declong2    ord-pl2 text2   place2-startdate    place2-enddate  comment2
        place_copied = [row[0] , row[28], row[29], row[30], 
        row[32], row[31], row[40], row[33], row[34], row[41],
        '','','']
        denormalized_data.append(place_copied)
        
        # put in intermediate stages
        for x in xrange(49, len(row), 13):
            constr = []
            constr.append(row[0])
            for item in row[x:x+12]:
                constr.append(item)
            denormalized_data.append(constr)

        # put current library
        current_library = [row[0], row[3], row[4], row[5], '', '', 
        'Current', row[6], row[7], row[8], '', '', '']
        denormalized_data.append(current_library)

    write_unique_points(denormalized_data, inf_name)
    # return dataset
    return denormalized_data

def write_output(final_data, outfile):
    """Write line segments to CSV file"""
    with open(outfile, 'w') as outf:
        ucsv.writer(outf, encoding = 'UTF-8').writerows(final_data)

def add_wkt_lines(database):
    for idx, row in enumerate(database):
        if idx == 0:
            row.append('WKT')
        else: 
            row.append('LINESTRING({0} {1}, {2} {3})'.format(row[8], row[7], row[21], row[20]))
    return database

## Classes
class Manuscript(object):
    def __init__(self, movements, ms_number):
        self.data = movements
        self.uid = ms_number
        self.segments = []

    def __repr__(self):
        return 'Processing CLA ID {0}'.format(self.uid)

    def parse_manuscript_record(self):
        #for row in self.data: print row[0], row[8]
        self.data.sort(key = lambda row:row[9])

        # find first point-event that isn't coded 'd' or 'f'
        i = 0
        try:
            while self.data[i][6] in ['d','f','m']:
                i += 1
            last_ok_point = self.data[i]
        # if no point not coded d or f is found
        except IndexError:
            return False

        for x in xrange(0, len(self.data)):
            if self.data[x] != last_ok_point:
                if self.data[x][6] in ['d','f','m']:
                    seg = self.data[x] + last_ok_point
                else:
                    seg = last_ok_point + self.data[x]
                    last_ok_point = self.data[x]

                self.segments.append(seg)
        # return bool to evaluate whether there are valid segments
        return True if len(self.segments) > 0 else False

def process_cla_volume(infile):
    print '>> Processing CLA Spreadsheet: {0}'.format(infile)
    #raw_data = import_csv(infile)[1:]
    raw_data = import_excel(infile)[1:]
    #print '>> Denormalizing dataset'
    denormalized_data = denormalize_dataset(raw_data, infile[:-4]) 

    headers = ['FR_MSID', 
               'FR_Library',
               'FR_City',
               'FR_Country', 
               'FR_Centroid',
               'FR_Certainty',
               'FR_Relation',    
               'FR_Latitude', 
               'FR_Longitude', 
               'FR_Order',  
               'FR_Comment', 
               'FR_Start',
               'FR_End',
               'TO_MSID', 
               'TO_Library',
               'TO_City',
               'TO_Country', 
               'TO_Centroid',
               'TO_Certainty',
               'TO_Relation',    
               'TO_Latitude', 
               'TO_Longitude', 
               'TO_Order',  
               'TO_Comment', 
               'TO_Start',
               'TO_End',
]
    
    # exclude rows without two coordinate pairs
    valid_data = [x for x in denormalized_data if x[7] != '' and x[8] != '']
    
    ms_movements = []
    #print '>> Parsing Manuscript Records'
    for ms in set([x[0] for x in valid_data]):
        m = Manuscript([p for p in valid_data if p[0] == ms], ms)
        if m.parse_manuscript_record():
            for segment in m.segments:
                ms_movements.append(segment)

    # add headers and write CSV file
    ms_movements.insert(0, headers)
    #print '>> Creating WKT Geometries'
    ms_movements = add_wkt_lines(ms_movements)
    #print '>> Writing output file'
    write_output(ms_movements, os.path.join('Movements', infile[:-4]+'_movements.csv'))

if __name__ == '__main__':
    if not os.path.isdir('Movements'):
        os.mkdir('Movements')
    if not os.path.isdir('Nodes'):
        os.mkdir('Nodes')

    start = time.time()    
    #for fname in glob.glob(os.path.join('cla_volume_[0-1][0-9].csv')):
    for fname in glob.glob(os.path.join('complete_cla_copy.xls')):
        process_cla_volume(fname)
    print '\n'
