import unicodecsv as csv
import sys
import glob
import math

def extract(target_manuscripts):
    target_rows = []
    first_of_all_rows = True
    for f in glob.glob('cla_volume_?.csv'):
        with open(f, 'rU') as inf:
            for row in csv.reader(inf):
                if first_of_all_rows:
                    target_rows.append(row)
                    first_of_all_rows = False
                try:
                    if math.floor(float(row[0])) in target_manuscripts:
                        target_rows.append(row)
                except ValueError:
                    pass
    return target_rows

if __name__ == '__main__':
    v = extract([int(x) for x in sys.argv[1:]])
    with open('manuscript_extract.csv','w') as outf:
        writer = csv.writer(outf)
        writer.writerows(v)