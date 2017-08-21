#!/usr/bin/env python
"""
      Generates test data choose a chunk and it distributes it randomly so that 

      Feature Space Tree can build the required vectors 

      USAGE  : generate-test_data.py path_to_test_data path_to_target_folders which_chunk_to_distribute
"""

# <imports>
import os
import sys 
from random import shuffle 
from shutil import copy 
#</imports>

#< helper functions>

join = lambda x,y: os.path.join(x,y)

def get_source_files(data_path,required_chunk):

	chunk_dir = join(data_path,required_chunk)

	files = [ join(chunk_dir,file) for file in os.listdir(chunk_dir) 
	          if os.path.isfile(
                join(chunk_dir,file)
	         ) ]

	return files

def get_destination_folders(target_path):

	folders = [ join(target_path,folder) for folder in os.listdir(target_path) 
                if os.path.isdir(
                join(target_path,folder)
               )
	          ]

	return folders

#</helper functions>

# <main>
if __name__ == '__main__':

	if os.path.isdir(sys.argv[1]):
		data_path = sys.argv[1]
	else:
		print 'test data directory is invalid'
		exit(1)

	if os.path.isdir(sys.argv[2]):
		target_path = sys.argv[2]
	else:
		print 'target directory is invalid'
		exit(2)

	if sys.argv[3] is not None:
		required_chunk = sys.argv[3]

	source_files = get_source_files(data_path,required_chunk)
	destination_folders = get_destination_folders(target_path)

	file_count = len(source_files)
	folder_count = len(destination_folders)

	folder_capacity = file_count // folder_count

	shuffle(source_files)
	shuffle(destination_folders)

	start = 0
	end = folder_capacity

	divided_files = []
	while len(divided_files) < (folder_count-1):
		divided_files.append(source_files[start:end])
		start=end
		end+=folder_capacity

	for idx in xrange(len(divided_files)):
		for to_move in divided_files[idx]:
			copy(to_move,destination_folders[idx])
			
	# write the random residual files to the last randomly chosen folder
	last_folder = destination_folders[-1]

	for file in source_files[start:]:
		copy(file,last_folder)

#</main>