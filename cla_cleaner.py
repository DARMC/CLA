import csv, time, os, xlrd, xlwt


if __name__ == '__main__':
	start = time.time()

	# split turn sep char into ;
	with open('CLA1.tsv', 'rU') as googleVersion, open('CLA1.txt', 'w') as scSep:
		for row in googleVersion:
			tmp = (row.replace(';', ','))
			scSep.write(tmp.replace('\t',';'))

	# split out place rows
	with open('CLA1.txt', 'rU') as inf, open('outfile.csv', 'w') as outf, open('MSattribs.csv', 'w') as outf2:
		reader  = csv.reader( inf  , delimiter = ';' )
		writer  = csv.writer( outf , delimiter = ';' )
		writer2 = csv.writer( outf2, delimiter = ';' )
		for row in reader:
			#write place copied
			plCopied = [row[0] , row[57], row[58], row[60], row[59], row[68], 
						row[61], row[62], row[69], row[70], ''     , '']

			writer.writerow(plCopied)
		
			# write movements
			writer2.writerow(row[0:75])
			for x in xrange(76, 210, 12):
				output = []
				output.append(row[0])
				for item in row[x:x+11]:
					output.append(item)
				writer.writerow(output)

			# write current library
			currentDisp = [row[0], row[4], row[3], '', '', 'Current', row[5], row[6], row[7],
						   '', row[13], row[14] ]
			writer.writerow(currentDisp)
		
	# clean place rows
	with open('outfile.csv', 'rU') as inf, open('CLA1_mvmt_output.csv', 'w') as outf:
		reader = csv.reader( inf , delimiter = ';' )
		writer = csv.writer( outf, delimiter = ';' )
		for row in reader:
			if any(field.strip() for field in row[1:]):
				writer.writerow(row)

	# now append from coordinates
	with open('CLA1_mvmt_output.csv', 'rU') as inf, open('CLA1_codeable.txt', 'w') as outf:
		reader = csv.reader(  inf, delimiter = ';' )
		writer = csv.writer( outf, delimiter = '\t' )
		for row in reader:
			if row[6] != '' and row[7] != '':
				writer.writerow(row)


	# clean intermediate files
	os.remove('outfile.csv')
	#os.remove('CLA1_mvmt_output.csv')
	os.remove('CLA1.txt')
		
	print 'Runtime: %.4f' % (time.time() - start)