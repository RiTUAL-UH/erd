from scipy.io import arff
import numpy as np 
from sklearn.tree import DecisionTreeClassifier as DT 
import argparse
import pandas
"""
Given an arff file rank attributes by info gain """

def read(path):

	data,meta = arff.loadarff(path)
	data_nolabels =np.asarray( [np.asarray(list(item)[:-1]) for item in data])
	labels = np.asarray([ item[-1] for item in data])
 	ds = pandas.DataFrame(data_nolabels,columns= list(meta)[:-1])
	return ds,labels

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python readscorer.py --path <> ')
	parser.add_argument('-p','--path',help='path to arff file',required=True)
	args= vars(parser.parse_args())
	train,truth = read(args['path'])
	clf = DT(criterion='entropy',splitter='best')
	clf = clf.fit(train,truth)
	for name,imp in zip(train.columns,clf.feature_importances_):
		print '{0} : {1}'.format(name,imp)