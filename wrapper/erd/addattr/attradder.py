import argparse
import os

""" adds attributes from readscorer's output to arff files 
viz input arffs to erd-system produced by feature space tree 

"""

def get_attrs(attr_file,istest):

	with open(attr_file) as af:
		id_fog_lwf = [tuple(line.split()) for line in af ]
		if istest == 'no':
			attrs = { item[0] : (item[1],item[2]) for item in id_fog_lwf}
		elif istest == 'yes':
			attrs = { item[0][item[0].find('s'):-4] : (item[1],item[2]) for item in id_fog_lwf}
		return attrs

def add_attrs(attrs,arff_file,output_file,istest):

	with open(arff_file) as af:
		data_flag = False
		with open(output_file,'w') as out:

			for line in af:
				
				pieces = line.split()

				if data_flag:

					if istest == 'no':
						fog_lwf = attrs[pieces[-1]]
					elif istest == 'yes':
						testkey = pieces[-1]
						testkey = testkey[testkey.find('s'):-4]
						fog_lwf = attrs[testkey]

					pieces.insert(-2,fog_lwf[0]+',')
					pieces.insert(-2,fog_lwf[1]+',')
					out.write(' '.join(s for s in pieces))
					out.write('\n')
				else:
					if len(pieces) > 1 and pieces[1] == 'categories':
						out_this = ['@attribute fog numeric      %% real name: \'fog scores\'',
									 '@attribute lwf numeric      %% real name: \'lwf scores\'',
									 line]
						out.write('\n'.join(s for s in out_this))
					else:
						out.write(line)

				if pieces[0] == '@data':
					data_flag = True

	return

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python attradder.py --attr <> --arff <> --out <> --test no')
	parser.add_argument('-a','--attr',help='path to ids and attributes  file',required=True)
	parser.add_argument('-b','--arff',help='path to arff  file',required=True)
	parser.add_argument('-o','--out',help='output file name',required=True)
	parser.add_argument('-t','--test',help='if test file type yes else no',required=True)	
	args= vars(parser.parse_args())

	add_attrs(get_attrs(args['attr'],args['test']),args['arff'],args['out'],args['test'])
