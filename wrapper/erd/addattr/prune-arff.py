import os
import sys
"""
Removes clutter from arff file so scipy.io.arff can load an arff into python

USAGE : python prune-arff.py <path to arff file> <name of out file>

"""
if __name__ == '__main__':

	if os.path.isfile(sys.argv[1]):
		arff_file=sys.argv[1]
	else:
		print('arff file does not exist')
		exit(1)

	outfile = sys.argv[2]

	with open(arff_file) as af:
		data_flag = False
		with open(outfile,'w') as out:
			for line in af:

				pieces = line.split()

				if data_flag:
					trim = pieces[:-1]
					out.write(' '.join(s for s in trim))
					out.write('\n')
				else:
					if pieces[0]!='@data' and pieces[0]!='@relation' and pieces[1] != 'categories':
						trim = pieces[:-4]
						out.write(' '.join(s for s in trim))
						out.write('\n')
					else:
						out.write(line)

				if pieces[0] == '@data':
					data_flag = True

					








