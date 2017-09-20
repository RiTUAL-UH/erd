from textstat.textstat import textstat
import argparse
import os
import numpy as np

"""
     Given a path to a dir containing chunk folders 
     generate a file for every chunk folder such as:

     chunkname_subjectname avg_lwf avg_fog

     which will be used with another script to combine as new attributes to representation files 
"""
lwf = lambda x: textstat.linsear_write_formula(x)
fog = lambda y: textstat.gunning_fog(y)
join = lambda g,z : os.path.join(g,z)
isfile = lambda z: os.path.isfile(z)
isdir = lambda z: os.path.isdir(z)

def get_chunknames(path):

	for direc in os.listdir(path):
		if isdir(direc):
			yield direc

def process(path,chunkname):

	subjects = [ file for file in os.listdir(join(path,chunkname)) if isfile(join(join(path,chunkname),file))]
	chunkid = chunkname.replace('-','_') + '_'
	# both ids and scores are in order of subjects above 
	ids = [  chunkid + z.replace('.','_') for z in subjects]
	avg_fogs,avg_lwfs = get_scores(path,chunkname,subjects)

	with open('./readscores_'+chunkname+'.txt','w') as out:
		for idx in xrange(len(subjects)):
			out.write('{} {} {}'.format(ids[idx],avg_fogs[idx],avg_lwfs[idx]))
			out.write('\n')
	return

def get_scores(path,chunkname,subjects):

	avg_fogs = []
	avg_lwfs = []

	for subject in subjects:

		read_path = join(join(path,chunkname),subject)
		fogs = []

		with open(read_path) as to_read:
			lines = (line.rstrip() for line in to_read)
			posts = list(line for line in lines if line)
			fogs = [ fog(post) for post in posts if fog(post) != None ]
			lwfs = [lwf(post) for post in posts ]


		avg_fogs.append(np.mean(fogs))
		avg_lwfs.append(np.mean(lwfs))

	return avg_fogs,avg_lwfs

if __name__ == '__main__':

	parser = argparse.ArgumentParser(description='USAGE :   python readscorer.py --path <folder contatining chunk folders> ')
	parser.add_argument('-p','--path',help='folder contatining chunk folders',required=True)
	args= vars(parser.parse_args())

	for chunk in get_chunknames(args['path']):
		process(args['path'],chunk)
		