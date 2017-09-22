import argparse
import os

""" adds attributes from readscorer's output to arff files 
viz input arffs to erd-system produced by feature space tree"""

def get_attrs(attr_file):

	with open(attr_file) as af:
		id_fog_lwf = [tuple(line.split()) for line in af ]
		attrs = { item[0] : (item[1],item[2]) for item in id_fog_lwf}
		return attrs

def add_attrs(attrs,arff_file):
	pass 

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python attradder.py --attr <> --arff <> ')
	parser.add_argument('-a','--attr',help='path to ids and attributes  file',required=True)
	parser.add_argument('-b','--arff',help='path to arff  file',required=True)	
	args= vars(parser.parse_args())

	print get_attrs(args['attr'])
