from __future__ import division 
from random import shuffle
from shutil import copy  
import os 
import argparse
import traceback

"""
        Generate dev set in such a way that 

   		1) if user is picked for train then all chunks of the user fall into train
   		2) if in oversampled mode appropriate over sampled input for the correct users should be in train set
   		3) test set should not be in oversampling 
   		4) maintain ratio of positive - negative users

"""
join = lambda x,y: os.path.join(x,y)
isdir = lambda x: os.path.isdir(x)
isfile = lambda y: os.path.isfile(y)
exists = lambda z : os.path.exists(z)

full_chunk = 'chunk1-2-3-4-5-6-7-8-9-10'

# used to prevent race condition between makedirs and exists 
directory_cache = set()

def get_usernames(path,sign):
	# get user names from <path>/<positive folder>/<chunk1-2>

	subdirs = [ join(path,subdir) for subdir in os.listdir(path) if isdir(join(path,subdir))]
	required_dir = [ subdir for subdir in subdirs if sign in subdir ] [0]
	target_folder = required_dir+'/'+'chunk1-2'

	if not isdir(target_folder):
		print sign+'users subfolder does not have chunk1-2 !!'
		exit(1)

	return [ u.split('.')[0] for u in os.listdir(target_folder) if isfile(join(target_folder,u)) ]

def get_popped_list(anylist, how_much_pop):
	# keep it dry loop helper 
	new = []
	counter = 0
	while  counter < how_much_pop:
		new.append(anylist.pop())
		counter+=1
	return new

def get_all_files(path,sign,username,chunks):
	# fetch files for user from their respective chunks 

	subdirs = [ join(path,subdir) for subdir in os.listdir(path) if isdir(join(path,subdir))]
	required_dir = [ subdir for subdir in subdirs if sign in subdir ] [0]

	try:
		for chunk in chunks:
			folder = required_dir + '/' + chunk
			for entry in os.listdir(folder):
				if isfile(join(folder,entry)) and username in entry:
					yield join(folder,entry)
		
	except Exception:
		print 'directory structure not proper (maybe)'
		traceback.format_exc()

def makeandcopy(filetocopy,out,neg=None):
	# keep it dry loop helper 
	dirtomake = filetocopy.split('/')[-2]

	if neg is not None:
		dirtomake+=neg

	if join(out,dirtomake) not in directory_cache:
		os.makedirs(join(out,dirtomake))
		directory_cache.add(join(out,dirtomake))

	copy(filetocopy,join(out,dirtomake))



if __name__ == '__main__':

	# get input 
	parser = argparse.ArgumentParser(description='USAGE :   python deveset_generator.py --path ./train --splitpercentage 70 --oversampling yes --fparam 4 ')
	parser.add_argument('-p','--path',help='path to train data folder',required=True)
	parser.add_argument('-sp','--splitpercentage',help='size of the devset in percentage',required=True)
	parser.add_argument('-o','--oversampling',help='if oversampling say yes else no',required=True)
	parser.add_argument('-f','--fparam',help='f parameter')
	args= vars(parser.parse_args())

	# list of all users 
	positive_users =  get_usernames(args['path'],'positive')
	negative_users =  get_usernames(args['path'],'negative')

	# randomize em 
	shuffle(positive_users)
	shuffle(negative_users)

	# math to split accurately 
	total_users = len(positive_users) + len(negative_users)
	train_size = ( total_users * int(args['splitpercentage']) ) // 100 
	test_size = total_users - train_size 

	#ceiling instead of floor
	test_positive_users = ((len(positive_users) * test_size ) // total_users) + 1 
	#floor 
	test_negative_users = (len(negative_users) * test_size ) // total_users 

	train_positive_users = len(positive_users) - test_positive_users
	train_negative_users = len(negative_users) - test_negative_users

	# dev-train = oversample_users + train_neg
	oversample_users = get_popped_list(positive_users,train_positive_users)
	train_neg = get_popped_list(negative_users,train_negative_users)

	# dev - test = test_pos + test_neg 
	test_pos = get_popped_list(positive_users,test_positive_users)  
	test_neg = get_popped_list(negative_users,test_negative_users)

	# chunks, oversampling_chunks , test_chunks arguments for getallfiles which fetches the files 
	chunks = ['chunk_'+str(x) for x in xrange(1,11) ]

	if args['fparam'] is not None:
		base = 'chunk1'
		oversampling_chunks = [ 'chunk_1']
		for i in xrange(2,int(args['fparam']) + 1):
			base+='-'+str(i)
			oversampling_chunks.append(base)
		oversampling_chunks.append(full_chunk)

	base = 'chunk1'
	testchunks = ['chunk_1']
	for i in xrange(2,11):
		base+='-'+str(i)
		testchunks.append(base)

	# output directories 
	out_train = './dev-train'
	out_test = './dev-test'

	if not isdir(out_train):
		os.makedirs(out_train)

	if not isdir(out_test):
		os.makedirs(out_test)

	# output the right files 
	if args['oversampling'] == 'yes':

		for user in oversample_users:
			for filetocopy in get_all_files(args['path'],'positive',user,oversampling_chunks):
				makeandcopy(filetocopy,out_train)

	elif args['oversampling'] == 'no':

		for user in oversample_users:
			for filetocopy in get_all_files(args['path'],'positive',user,[full_chunk]):
				makeandcopy(filetocopy,out_train)
		 

	for user in train_neg:
		for filetocopy in get_all_files(args['path'],'negative',user,[full_chunk]):
			makeandcopy(filetocopy,out_train,'neg')


	for user in test_pos:
		for filetocopy in get_all_files(args['path'],'positive',user,testchunks):
			makeandcopy(filetocopy,out_test)

	for user in test_neg:
		for filetocopy in get_all_files(args['path'],'negative',user,testchunks):
			makeandcopy(filetocopy,out_test)












	

	








	
