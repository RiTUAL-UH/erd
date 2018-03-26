from nltk import word_tokenize

def get_bag(list_of_files):
	"""
         Args: [file_path1,....]

         Returns: vocabulary of all terms used in given files
	"""
	bag = set()
	for file_name in list_of_files:
		with open(file_name) as inp:
			for line in inp:
				if line:
					for term in word_tokenize(line.strip()):
						bag.add(term)
	return bag





if __name__ == '__main__':
	
	TP, FP, FN, TN = [], [], [], []

	with open('error_analysis.txt') as ea:
		for line in ea:
			row = line.strip().split()
			subject,pred,truth = row[0].split('_')[-1]+'.txt',row[1],row[2]

			if pred==truth:
				if pred == '1':
					TP.append(subject)
				elif pred=='0':
					TN.append(subject)
			else:
				if pred =='0':
					FN.append(subject)
				elif pred=='1':
					FP.append(subject)

	print(len(TP)+len(FN)+len(FP)+len(TN))

	depressed_confusion = get_bag(TP).intersection(get_bag(FP))

	while depressed_confusion:
		print(depressed_confusion.pop())
	#TP_bag = set()
	#FP_bag = set()




