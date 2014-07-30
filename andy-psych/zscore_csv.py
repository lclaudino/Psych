"""
Takes a Pennebaker metadata CSV and z-scores each of the following attributes:

neuro
extra
consc
agree
open

The CSV is rewritten with only year, id, and those five attributes.

An author is only in the new CSV if he had all of the five attributes.
"""

import csv
import sys
import math
from optparse import OptionParser

def processCSV(input_filename,output_filename):
	in_file=open(input_filename,'r')
	in_csv=csv.DictReader(in_file)
	
	#calculate neuro average
	neuro_list=[]
	num_neuros=0
	
	for row in in_csv:
		neuro_val=-1
		neuro_str=row['neuro']
		if neuro_str.strip()!='':
			try:
				neuro_list.append(float(neuro_str))
			except:
				continue

	#calculate neuro mean
	neuro_mean=float(sum(neuro_list)/len(neuro_list))

	#calculate neuro stdev
	neuro_squared_diffs=[(i-neuro_mean)**2 for i in neuro_list]

	neuro_stdev=math.sqrt(float(sum(neuro_squared_diffs)/len(neuro_squared_diffs)))

	print 'Mean: '+str(neuro_mean)
	print 'Stdev: '+str(neuro_stdev)

	#have mean and stdev, now output new CSV with attributes: year,id,zneuro


	in_file.seek(0)

	output_array=[]
	for row in in_csv:
		neuro_val=-1
		neuro_str=row['neuro']

		if neuro_str.strip()!='':
			try:
				neuro_val=float(neuro_str)
				neuro_z = (neuro_val - neuro_mean)/(neuro_stdev)
				auth_id=row['id']
				year=row['year']

				this_dct={}
				this_dct['auth_id']=auth_id
				this_dct['year']=year
				this_dct['zneuro']=neuro_z
				output_array.append(this_dct)

			except:
				continue

	print 'Size of output array: ' + str(len(output_array))

	#use DictWriter to write output_array to CSV
	fieldnames = ['auth_id', 'year', 'zneuro']
	output_CSV = open(output_filename,'w')
	writer=csv.DictWriter(output_CSV, delimiter=',', fieldnames=fieldnames)
	writer.writerow(dict((fn,fn) for fn in fieldnames)) #write headers
	for row in output_array:
		writer.writerow(row)
	output_CSV.close()





#main function
def Main():
	parser=OptionParser()
	parser.add_option("-i", "--input", dest="input")
	parser.add_option("-o","--output",dest="output")
	(options,args) = parser.parse_args()

	if not options.input or not options.output:
		print 'provide an input filename and an output filename.'
		sys.exit(1)

	#load CSV into dictionary
	processCSV(options.input,options.output)



if __name__=="__main__":
	Main()

