import glob
import unicodecsv as csv
import os
import xlwt

def write_xls_sheet(data):
	book = xlwt.Workbook(encoding='utf-8')
	sheet = book.add_sheet('CLA')
	for i, row in enumerate(data):
	    for j, field in enumerate(row):
	        sheet.write(i, j, field.encode('utf-8'))
	book.save('complete_cla.xls')	

if __name__ == '__main__':
	print '=== CREATING COMPLETE CLA EXCEL SPREADSHEET ==='
	first = True
	all_volumes = []
	for volume, f in enumerate(glob.glob(os.path.join('cla_volume_??.csv'))):
		print f
		with open(f, 'rU') as inf:
			for idx, row in enumerate(csv.reader(inf)):
				if idx == 0 and first:
					header = row[:]
					header.insert(0,'Volume')
					all_volumes.append(header)
					first = False
				elif idx==0 and not first:
					pass
				else:
					new_row = row[:]
					new_row.insert(0, str(volume+1))
					all_volumes.append(new_row)

	write_xls_sheet(all_volumes)
