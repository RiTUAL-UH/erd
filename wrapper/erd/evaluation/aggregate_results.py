import os
import xml.etree.ElementTree as et
import argparse
import random
import re
import traceback


parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('-path', help='(Obligatory) Path to folder where XML files are placed.', required=True, nargs=1, dest="path")
parser.add_argument('-wsource', help='(Obligatory) Source file of number of writings.', required=True, nargs=1, dest="wsource")
args = parser.parse_args()




path = args.path[0]
wsource = args.wsource[0]
chunks = 10


#Lista de documentos en el path
lista = os.listdir(path)
if path[-1]=="/":
	path = list(path)
	path[-1]=""

path="".join(path)

usuarios = {}


us_wr = open(wsource,"r")

#Leemos los uduarrios
lines = us_wr.readlines()
for line in lines:
	line = (line.replace("\n","")).split("\t")

	#usuarios[nombre]=[numWritings,estado,chunks_hasta_leerlo]
	usuarios[line[0]]=[int(line[2]),0,0]

us_wr.close()



#Listas para _ 
index_=[]
org_name = ""

for item in lista:
	if not ".DS_Store" in item:
		itemlist = list(item)
		for letter in range(0,len(itemlist)):
			if itemlist[letter] == "_":
				index_.append(letter)
		org_name = item[0:index_[-1]]
		break;



#Comenzamos a leer los ficheros del usuario
for i in range(1,chunks+1):

	#Para el chunk i 
	f_user = open(path+"/"+org_name+"_"+str(i)+".txt","r")
	lines=f_user.readlines()

	#Iteramos sobre los registros del fichero
	for line in lines:
		try:
			line = (line.replace("\n","")).split("\t")
			subject = usuarios[line[0]]
			
			if int(subject[1])==0:
				subject[1]=int(line[2])
				subject[2]=i
		except KeyError:
			print traceback.format_exc()
	f_user.close()

final = open(path+"/"+org_name+"_global.txt","w")
for key in usuarios:
	subject = usuarios[key]
	
	if subject[2]==chunks:
		num_w = subject[0]
	else:
		num_w =(subject[0]/chunks) * subject[2]
		

		if int(subject[1])==2:
			subject[1]=0

	final.write(key+" "+str(subject[1])+" "+str(num_w)+"\n")
final.close()

print "Results saved in output file \""+path+"/"+org_name+"_global.txt\""


				

		
					
			




	

