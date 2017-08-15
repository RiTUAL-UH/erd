#!/usr/bin/env python
"""
    USAGE :  \> python label_arff.py truth_file arff_file output_file
"""
import sys
import os

replace_positive = '1'
replace_negative = '0'
replace_categories = '{0,1}' 

def get_truth_sets(content):

	positive = set()
	negative = set()

	for line in content:
		subject,flag= line.split()

		if int(flag) == 1:
			positive.add(subject.split('_')[-1])
		elif int(flag) == 0:
			negative.add(subject.split('_')[-1])
	
	return (positive,negative)


def get_subject_name(text):

	for item in text.split('_'):
		if item[:7] == 'subject':
			return item


if __name__=='__main__':

	if os.path.isfile(sys.argv[1]):
		truth_file=sys.argv[1]
	else:
		print('arff file does not exist')
		exit(1)

	if os.path.isfile(sys.argv[2]):
		arff_file = sys.argv[2]
	else:
		print('truth file does not exist')
		exit(2)

	output_file = sys.argv[3]

	with open(truth_file) as tf:
		pos,neg=get_truth_sets([ x.strip('\n') for x in tf.readlines()])

	with open(arff_file) as af:
		data_flag = False
		with open(output_file,'w') as out:
			for line in af:

				pieces = line.split()

				if data_flag:

					name = get_subject_name(pieces[-1])

					if name in pos:
						pieces[-2] = replace_positive
					elif name in neg:
						pieces[-2] = replace_negative

					out.write(' '.join(s for s in pieces))
					out.write('\n')

				else:
					if len(pieces) > 1 and pieces[1] == 'categories':
						out_this = [pieces[0],pieces[1],replace_categories]
						out.write(' '.join(s for s in out_this))
						out.write('\n')
					else:
						out.write(line)

				if pieces[0] == '@data':
					data_flag = True

		
				
						



