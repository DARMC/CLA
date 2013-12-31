import unicodecsv as csv
import sys
import glob
import math
import argparse
import sqlite3 as sqlite
import xlwt
import os

def extract_from_sqlite_db(database, target_manuscripts):
    """
    Get rows from specified sqlite database files matching user input numbers
    
    Not ready for primetime yet. No guarantees this code wil do anything.
    """
    # check database already exists so you don't accidentally create a new one
    if not os.path.isfile(database):
        sys.exit('Specified database was not found')
    # otherwise extract the manuscripts
    else:
        # set up database connection
        extracted_rows = []
        conn = sqlite.connect(database)
        c = conn.cursor()
        
        # get column names
        ##
        # TODO
        ##

        # extract manuscripts
        for manuscript in target_manuscripts:
            c.execute('''SELECT * FROM complete_records WHERE [MSID] >= ? AND [MSID] >= ?''',(manuscript, manuscript+1))
            extracted_rows += c.fetchall()

    return extracted_rows

def extract_from_csvs(target_manuscripts):
    """
    Get rows from all base csv files matching user input numbers
    """
    extracted_rows = []
    write_header = True
    # iterate over each cla volume file
    for f in glob.glob('cla_volume_?.csv'):
        with open(f, 'rU') as inf:
            for row in csv.reader(inf):
                if write_header:
                    extracted_rows.append(row)
                    write_header = False
                try:
                    if math.floor(float(row[0])) in target_manuscripts:
                        extracted_rows.append(row)
                except ValueError:
                    pass
    return extracted_rows

if __name__ == '__main__':
    # set up argument parsing
    parser = argparse.ArgumentParser(description='CLA Manuscript extractor')
    parser.add_argument('manuscripts', type = int, nargs = '+',
                help='Any number of integers representing the database \
                      MSID. Attempts to honor decimal pieces of manuscripts')
    parser.add_argument('--sqlite', type = str, nargs = 1,
                help='Use specified sqlite database if present')
    args = parser.parse_args()

    # either use sqlite database or csvs
    if args.sqlite:
        v = extract_from_sqlite_db([x for x in args.manuscripts])

    else:
        v = extract_from_csvs([x for x in args.manuscripts])

    book = xlwt.Workbook(encoding='utf-8')
    sheet = book.add_sheet('extract')
    for i, row in enumerate(v):
        for j, field in enumerate(row):
            sheet.write(i, j, field.encode('utf-8'))
    book.save('manuscript_extract.xls')
