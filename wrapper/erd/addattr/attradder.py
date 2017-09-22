import argparse
import os

""" adds attributes from readscorer's output to arff files 
viz input arffs to erd-system produced by feature space tree 

NOTE: for now manually add @attrs in output file as it is weird to do it in a single pass 
"""

def get_attrs(attr_file):

	with open(attr_file) as af:
		id_fog_lwf = [tuple(line.split()) for line in af ]
		attrs = { item[0] : (item[1],item[2]) for item in id_fog_lwf}
		return attrs

def add_attrs(attrs,arff_file,output_file):

	with open(arff_file) as af:
		data_flag = False
		with open(output_file,'w') as out:

			for line in af:
				
				pieces = line.split()

				if data_flag:
					fog_lwf = attrs[pieces[-1]]
					pieces.insert(-2,fog_lwf[0]+',')
					pieces.insert(-2,fog_lwf[1]+',')
					out.write(' '.join(s for s in pieces))
					out.write('\n')
				else:
					out.write(line)

				if pieces[0] == '@data':
					data_flag = True

	return

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python attradder.py --attr <> --arff <> --out <> ')
	parser.add_argument('-a','--attr',help='path to ids and attributes  file',required=True)
	parser.add_argument('-b','--arff',help='path to arff  file',required=True)
	parser.add_argument('-o','--out',help='output file name',required=True)	
	args= vars(parser.parse_args())

	add_attrs(get_attrs(args['attr']),args['arff'],args['out'])
