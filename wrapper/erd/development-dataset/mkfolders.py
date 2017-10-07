import os
import sys

if __name__ =='__main__':

	base1 = 'chunk_'
	base2 = 'chunk1-2'

	os.chdir(sys.argv[1])

	for x in range(1,11):
		os.mkdir('./'+base1+str(x))

	for y in range(3,12):
		os.mkdir('./'+base2)
		base2+='-'+str(y)

