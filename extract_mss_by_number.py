import unicodecsv as csv
import sys
import glob
import math
import argparse

def extract(target_manuscripts):
    """
    Get rows from all files matching user input numbers
    """
    target_rows = []
    write_header = True
    for f in glob.glob('cla_volume_?.csv'):
        with open(f, 'rU') as inf:
            for row in csv.reader(inf):
                if write_header:
                    target_rows.append(row)
                    write_header = False
                try:
                    if math.floor(float(row[0])) in target_manuscripts:
                        target_rows.append(row)
                except ValueError:
                    pass
    return target_rows

if __name__ == '__main__':
    # set up argument parsing
    parser = argparse.ArgumentParser(description='CLA Manuscript extractor')
    parser.add_argument('manuscripts', type = int, nargs = '+')
    args = parser.parse_args()

    # extract manuscripts
    v = extract([x for x in args.manuscripts])
    with open('manuscript_extract.csv','w') as outf:
        writer = csv.writer(outf)
        writer.writerows(v)