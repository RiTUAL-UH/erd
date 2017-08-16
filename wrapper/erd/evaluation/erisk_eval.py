import pandas as pd
import numpy as np
import argparse
import traceback

	# To calculate the metrics of the classification algorithm
def erde_evaluation(goldenTruth_path, algorithmResult_path, o):
		# Transform files into tables
		try:
			data_golden = pd.read_csv(goldenTruth_path, sep=" ", header=None, names=['subj_id','true_risk'])
			data_result = pd.read_csv(algorithmResult_path, sep=" ", header=None, names=['subj_id','risk_decision','delay'])

			# Merge tables (data) on common field 'subj_id' to compare the true risk and the decision risk
			merged_data = data_golden.merge(data_result, on='subj_id', how='left')

			# Add column to store the idividual ERDE of each user
			merged_data.insert(loc=len(merged_data.columns), column='erde',value=1.0)

			# Variables
			risk_d = merged_data['risk_decision']
			t_risk = merged_data['true_risk']
			k = merged_data['delay']
			erde = merged_data['erde']

			# Count of how many true positives there are
			true_pos = len(merged_data[t_risk==1])

			#Count of how many true negatives there are 
			true_neg = len(merged_data[t_risk==0])
			
			# Count of how many positive cases the system decided there were
			pos_decisions = len(merged_data[risk_d==1])

			# negative by system
			neg_decisions = len(merged_data[risk_d==0])

			# Count of how many of them are actually true positive cases
			tpusers = merged_data[(t_risk==1) & (risk_d==1)]['subj_id']
			tnusers = merged_data[(t_risk==0) & (risk_d==0)]['subj_id']
			fpusers = merged_data[(t_risk==0) & (risk_d==1)]['subj_id']
			fnusers = merged_data[(t_risk==1) & (risk_d==0)]['subj_id']

			pos_hits = len(merged_data[(t_risk==1) & (risk_d==1)])

			neg_hits = len(merged_data[(t_risk==0) & (risk_d==0)])

			fp_hits = len(merged_data[(t_risk==0) & (risk_d==1)])

			fn_hits = len(merged_data[(t_risk==1) & (risk_d==0)])

			# Total count of users
			total_users = len(merged_data)

			undecided = total_users - (pos_hits+neg_hits+fp_hits+fn_hits)

			print '############################# CONFUSION MATRIX #############################'
			print '_____|___1___|___0___|'
			print '__1__|  {0}  |  {1}  |'.format(pos_hits,fn_hits)
			print '__0__|  {0}  |  {1}  |'.format(fp_hits,neg_hits)
			print 'undecided : {0}'.format(undecided)
			print 'total : {0}'.format(total_users)
			print ' writing user categories to files for comparison '
			print '$$$$$$$$$$$$$$$$$$$$$$$$$$ Users-TP.txt Generated $$$$$$$$$$$$$$$$$$$$$$$$$'
			with open('Users-TP.txt','w') as out:
				for u in tpusers:
					out.write(u)
					out.write('\n')
			print '$$$$$$$$$$$$$$$$$$$$$$$$$$ Users-TN.txt Generated $$$$$$$$$$$$$$$$$$$$$$$$$$$$'
			with open('Users-TN.txt','w') as out:
				for u in tnusers:
					out.write(u)
					out.write('\n')
			print '$$$$$$$$$$$$$$$$$$$$$$$$$$ Users-FP.txt Generated $$$$$$$$$$$$$$$$$$$$$$$$$$'
			with open('Users-FP.txt','w') as out:
				for u in fpusers:
					out.write(u)
					out.write('\n')
			print '$$$$$$$$$$$$$$$$$$$$$$$$$$ Users-FN.txt Generated $$$$$$$$$$$$$$$$$$$$$$$$$$$'
			with open('Users-FN.txt','w') as out:
				for u in fnusers:
					out.write(u)
					out.write('\n')
			print '#############################################################################'

			# ERDE calculus
			for i in range(total_users):
				if(risk_d[i] == 1 and t_risk[i] == 0):
					erde.ix[i] = float(true_pos)/total_users
				elif(risk_d[i] == 0 and t_risk[i] == 1):
					erde.ix[i] = 1.0
				elif(risk_d[i] == 1 and t_risk[i] == 1):
					erde.ix[i] = 1.0 - (1.0/(1.0+np.exp(k[i]-o)))
				elif(risk_d[i] == 0 and t_risk[i] == 0):
					erde.ix[i] = 0.0

			# Calculus of F1, Precision, Recall and global ERDE
			precision = float(pos_hits)/pos_decisions
			recall = float(pos_hits)/true_pos
			F1 = 2 * (precision * recall) / (precision + recall)
			erde_global = erde.mean() * 100

			indiv_erde = merged_data.ix[:,['subj_id','erde']]
			print indiv_erde.to_string()
			print 'Global ERDE (with o = %d): %.2f' % (o, erde_global), '%'
			print 'F1: %.2f' % F1
			print 'Precision: %.2f' % precision
			print 'Recall: %.2f' % recall

		except:
			print traceback.format_exc()
			print 'Some file or directory doesn\'t exist or an error has occurred'





parser = argparse.ArgumentParser(argument_default=argparse.SUPPRESS)
parser.add_argument('-gpath', help='(Obligatory) path to golden truth file.', required=True, nargs=1, dest="gpath")
parser.add_argument('-ppath', help='(Obligatory) path to prediction file from a system.', required=True, nargs=1, dest="ppath")
parser.add_argument('-o', help='(Obligatory) o parameter.', required=True, nargs=1, dest="o")

args = parser.parse_args()

gpath = args.gpath[0]
ppath = args.ppath[0]
o = int(args.o[0])


erde_evaluation(gpath, ppath, o)



