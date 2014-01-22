import xlrd
import xlwt

def read_worksheet(n, workbook, worksheet_name):
    """
    Read worksheet 'worksheet_name'
    """
    ws = workbook.sheet_by_name(worksheet_name)
    num_rows, num_cells = ws.nrows - 1, ws.ncols - 1
    volume = []
    # only keep the header from CLA volume 1
    curr_row = 0 if n == 1 else 1

    for i in xrange(curr_row, num_rows):
        row = []
        for j in xrange(0, num_cells):
            val = ws.cell_value(i, j)
            row.append(val)
        
        # add the volume number to the row
        if n == 1 and i == 0:
            row.insert(0, 'Volume')
        else:
            row.insert(0, n)

        volume.append(row)
    
    return volume

def write_worksheet(contents):
    """
    Write values in 2-dimensional list 'contents' to an Excel file.
    """
    book = xlwt.Workbook()
    worksheet = book.add_sheet('Complete CLA')

    # unpack array values into worksheet
    for row, array in enumerate(contents):
        for col, value in enumerate(array):
            worksheet.write(row, col, value)

    # save file
    book.save("Complete CLA Database.xls")

if __name__ == '__main__':
    workbook = xlrd.open_workbook('CLA Geodatabase 2013.xlsx')
    worksheets = workbook.sheet_names()
    complete_cla_array = []

    for enum, worksheet_name in enumerate(worksheets):
        if "CLA" in worksheet_name:
            complete_cla_array += read_worksheet(enum + 1, workbook, worksheet_name)

    write_worksheet(complete_cla_array)
