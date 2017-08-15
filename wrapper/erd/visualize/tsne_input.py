"""
USAGE : python tsne_input.py labeled_arff_file <oversampling yes or no>
"""
import sys
import os

full_chunk = 'chunk1_2_3_4_5_6_7_8_9_10'

if __name__=='__main__':

	if os.path.isfile(sys.argv[1]):
		arff_file=sys.argv[1]
	else:
		print('arff file does not exist')
		exit(1)

	with open(arff_file) as af:
		data_flag = False
		with open('mnist2500_labels.txt','w') as out_labels:
			with open('mnist2500_X.txt','w') as out_vectors:
				for line in af:

					pieces = line.split()

					if data_flag:

						if sys.argv[2] == 'yes':
							if full_chunk in pieces[-1]:
								out_labels.write(pieces[-2])
								out_labels.write('\n')
							else:
								out_labels.write('2')
								out_labels.write('\n')
								
						elif sys.argv[2] =='no':
							out_labels.write(pieces[-2])
							out_labels.write('\n')

						out_vectors.write('   '.join(s[:-1] for s in pieces[:-2]))
						out_vectors.write('\n')

					if pieces[0] == '@data':
						data_flag = True
