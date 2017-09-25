from scipy.io import arff
import numpy as np 
from sklearn.tree import DecisionTreeClassifier as DT 
import argparse
import pandas
from operator import itemgetter
from copy import deepcopy
"""
Given an arff file rank attributes by info gain """

def read(path):

	data,meta = arff.loadarff(path)
	data_nolabels =np.asarray( [np.asarray(list(item)[:-1]) for item in data])
	labels = np.asarray([ item[-1] for item in data])
	cols = list(meta)[:-1]
 	ds = pandas.DataFrame(data_nolabels,columns = cols )
	return ds,labels

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python readscorer.py --path <> ')
	parser.add_argument('-p','--path',help='path to arff file',required=True)
	args= vars(parser.parse_args())
	train,truth = read(args['path'])
	clf = DT(criterion='entropy',splitter='best')
	clf = clf.fit(train,truth)
	# clustering 
	k  = [x for x in xrange(1,33) if x%2 == 0]
	k = [1] + k
	# 6 attributes originally 
	k= map(lambda z: z*6,k) 
	k.reverse()
	clusters = {}
	feature_imps = [(name,imp) for name,imp in zip(train.columns,clf.feature_importances_)]

	start = 0
	end  =0

	while k:
		end = k.pop()
		clusters[end/6] = set((u,v) for u,v in feature_imps[start:end])
		start = end

	fimps = deepcopy(feature_imps)
	fimps.sort(key=itemgetter(1),reverse=True)

	print 'printing attributes ranked by info gain'
	counter = 1
	print 'index num_of_clusters feature info_gain'
	for name,imp in fimps:
		which_clustering = None
		for key in clusters.keys():
			if (name,imp) in clusters[key]:
				which_clustering = key
				break
		print '{0}) {1} {2} {3}'.format(counter,which_clustering,name,imp)
		counter+=1


	"""for key in clusters.keys():
		print 'number of clusters : {0}'.format(key)
		print 'feature importances are as follows, feature_name : info_gain'
		for x,y in clusters[key]:
			print '{0} : {1}'.format(x,y)
		print '########################################################'"""








