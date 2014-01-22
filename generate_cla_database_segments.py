import time
import unicodecsv as csv
import xlrd
import sys
import glob
import os

# OK
def import_csv(infile):
    """
    Return raw data array from csv file
    """
    return [line for line in csv.reader(open(infile,'rU'))]

def import_excel(infile):
    """
    Return raw data arraw from excel file
    """
    print '>> Importing data from file: {0}'.format(infile)
    workbook = xlrd.open_workbook(infile)
    ws = workbook.sheet_by_name('Complete CLA')
    complete_cla_data = []
    for i in xrange(ws.nrows):
        row_data = []
        for j in xrange(ws.ncols):
            row_data.append(ws.cell_value(i, j))
        complete_cla_data.append(row_data)
    print '>> Read {0} records'.format(len(complete_cla_data))
    return complete_cla_data

# TODO
def write_unique_points(d, inf_name):
    def is_in(existing, c):
        match = False
        if len(existing) > 0:
            for r in existing:
                if r[0:3] == c[0:3]:
                    match = True
        return match

    with open(os.path.join(inf_name+' Points.csv'),'w') as outf:
        writer = csv.writer(outf)
        writer.writerow(['ID','Library or Archive','City or Region','Country',
                         'Centroid Type', 'Latitude', 'Longitude', 'WKT String'])
        data_to_write = []
        for row in d:
            if row[8] != '' and row[9] != '':
                wkt_point = ['POINT({0} {1})'.format(row[9], row[8])]
                node_line = row[1:5] + row[8:10] + wkt_point
                data_to_write.append(node_line)
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
    for row in raw_data:
        # add place copied
        place_copied = [row[1], row[35], row[36], row[37], row[39], row[38],
                        row[48], row[49], row[40], row[41], row[50], '',
                        row[16], row[17], '', '', '']
        denormalized_data.append(place_copied)

        # put in intermediate stages
        for x in xrange(57, len(row), 16):
            constr = []
            constr.append(row[1])
            for item in row[x:x+16]:
                constr.append(item)
            denormalized_data.append(constr)

        # put current library
        current_library = [row[1], row[4], row[5], row[6], '', '', row[9],
                           'Current', row[7], row[8], row[10], '', '', '',
                           '', '', '']
        denormalized_data.append(current_library)

    write_unique_points(denormalized_data, inf_name)
    # return dataset
    return denormalized_data

def write_output(final_data, outfile):
    """
    Write line segments to CSV file
    """
    with open(outfile, 'w') as outf:
        csv.writer(outf, delimiter = ',', encoding = 'UTF-8').writerows(final_data)

# TOFIX
def add_wkt_lines(database):
    for idx, row in enumerate(database):
        if idx == 0:
            row.append('WKT')
        else:
            #print row 
            row.append('LINESTRING({0} {1}, {2} {3})'.format(row[9], row[8], row[27], row[26]))
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
        #print self.data
        #sys.exit()
        # find first point-event that isn't coded 'd' or 'f' or 'm'
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

def process_cla_volume(infile, mode = 'excel'):
    print '>> Processing CLA Spreadsheet: {0}'.format(infile)
    if mode == 'csv':
        raw_data = import_csv(infile)[1:]
    elif mode == 'excel':
        raw_data = import_excel(infile)[1:]
    #print '>> Denormalizing dataset'
    denormalized_data = denormalize_dataset(raw_data, infile[:-5]) 
    #for d in denormalized_data: print len(d)
    headers = ['FR_MSID', 
               'FR_Library',
               'FR_City',
               'FR_Country', 
               'FR_Centroid',
               'FR_Certainty',
               'FR_Context',
               'FR_Relation',    
               'FR_Latitude', 
               'FR_Longitude', 
               'FR_Order',  
               'FR_Text', 
               'FR_Start',
               'FR_End',
               'FR_DateQ',
               'FR_DateLit',
               'FR_Comment',
               'TO_MSID', 
               'TO_Library',
               'TO_City',
               'TO_Country', 
               'TO_Centroid',
               'TO_Certainty',
               'TO_Context',
               'TO_Relation',    
               'TO_Latitude', 
               'TO_Longitude', 
               'TO_Order',  
               'TO_Text', 
               'TO_Start',
               'TO_End',
               'TO_DateQ',
               'TO_DateLit',
               'TO_Comment'
               ]
    
    # exclude rows without two coordinate pairs
    valid_data = [x for x in denormalized_data if x[8] != '' and x[9] != '']
    
    ms_movements = []
    #print '>> Parsing Manuscript Records'
    for ms in set([x[0] for x in valid_data]):
        #print ms
        m = Manuscript([p for p in valid_data if p[0] == ms], ms)
        if m.parse_manuscript_record():
            for segment in m.segments:
                #print segment
                ms_movements.append(segment)

    # add headers and write CSV file
    ms_movements.insert(0, headers)
    #print '>> Creating WKT Geometries'
    ms_movements = add_wkt_lines(ms_movements)
    #print '>> Writing output file'
    write_output(ms_movements, os.path.join(infile[:-5]+'_movements.csv'))

if __name__ == '__main__':
    start = time.time()    
    #for fname in glob.glob(os.path.join('cla_volume_[0-1][0-9].csv')):
    for fname in glob.glob(os.path.join('Complete CLA Database.xlsx')):
        process_cla_volume(fname, mode = 'excel')
