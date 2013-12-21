import unicodecsv as csv
import sys
import glob
import math

def extract(target_manuscripts):
    target_rows = []
    for f in glob.glob('cla_volume_?.csv'):
        with open(f, 'rU') as inf:
            for row in csv.reader(inf):
                try:
                    if math.floor(float(row[0])) in target_manuscripts:
                        target_rows.append(row)
                except ValueError:
                    pass
    return target_rows

if __name__ == '__main__':
    v = extract([int(x) for x in sys.argv[1:]])
