import time
import os
import xlrd, xlwt
import unicodecsv as ucsv
import math
import shapefile_functions as sfuncs

def write_output(movements):
    with open('denorm_test.csv', 'w') as outf:
        wr = ucsv.writer(outf, delimiter=',')
        for movement in movements:
            wr.writerow(movement)

def read_manuscript_points(infile):
    """Return raw data array from csv file"""
    with open(infile,'rU') as inf:
        raw_data = [line for line in ucsv.reader(inf)]
    return raw_data

def denormalize_dataset(data):
    """Return one manuscript point per line"""
    # denormalize rows
    denormalized_data = []
    for row in data:
        # put place copied
        place_copied = [row[0] , row[57], row[58], row[60], row[59], row[68], 
                        row[61], row[62], row[69], row[70], ''     , '']
        denormalized_data.append(place_copied)
        
        # put in intermediate stages
        for x in xrange(76, 210, 12):
            constr = []
            constr.append(row[0])
            for item in row[x:x+11]:
                constr.append(item)
            denormalized_data.append(constr)

        # put current library
        current_library = [row[0], row[4], row[3], '', '', 'Current', row[5], row[6], row[7],
                           '', row[13], row[14] ]
        denormalized_data.append(current_library)

    return denormalized_data

def write_output_database(denormalized_data):
    with open('cla_output.csv', 'w') as outf:
        wr = ucsv.writer(outf)
        for d in denormalized_data:
            if d[6] != '' and d[7] != '':
                wr.writerow(d)  

class Manuscript(object):
    def __init__(self, movements, trip_id):
        self.data = movements
        self.uid = trip_id
        self.segments = []

    def __repr__(self):
        return 'Processing CLA ID {0}'.format(self.uid)

    def parse_manuscript_record(self):
        self.data.sort(key = lambda row:row[8])
        for x in xrange(0,len(self.data)-1):
            seg = self.data[x] + self.data[x+1]
            self.segments.append(seg)
        return True

    def return_trip_segments(self):
        return self.segments

if __name__ == '__main__':
    start = time.time()

    ## Create fully denormalized database of manuscript points
    # read in data
    raw_data = read_manuscript_points('cla_volume_1.csv')
    raw_data = raw_data[1:]
    # denormalize
    denormalized_data = denormalize_dataset(raw_data)
    #write denormalized output
    #write_output_database(denormalized_data)    
    headers = ['FR_MISD', 'FR_N', 'FR_REG', 'FR_CENT',
               'FR_CERT', 'FR_RLXN', 'FR_LAT', 'FR_LONG', 
               'FR_ORD', 'FR_COMMENT', 'FR_ST', 'FR_END',
               'TO_MISD', 'TO_N', 'TO_REG', 'TO_CENT', 
               'TO_CERT', 'TO_RLXN', 'TO_LAT', 'TO_LONG',
               'TO_ORD', 'TO_COMMENT', 'TO_ST', 'TO_END']
    
    ## Create a database of movements from points
    # get unique manuscripts
    movements = []
    spatial_data = [x for x in denormalized_data if x[6] != '']
    for manuscript in set([x[0] for x in spatial_data]):
        m = Manuscript([p for p in spatial_data if p[0] == manuscript], manuscript)
        m.parse_manuscript_record()
        mvmts = m.return_trip_segments()
        if len(mvmts) > 0:
            for mvmt in mvmts:
                if len(mvmts) > 0:
                    movements.append(mvmt)

    movements.insert(0, headers)
    write_output(movements)
    print 'Runtime: {0:.4}'.format(time.time() - start)