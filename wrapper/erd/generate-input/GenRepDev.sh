#!/bin/bash

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

echo making training arff_file

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  

#python ./featurespacetree/entry_point.py pyramidal-soa2.yaml --train

#python ./featurespacetree/entry_point.py settings_soa_GOOD.yaml --train

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

echo labeling the training arff_file

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

#python ./labeling/label_arff.py ./labeling/train_golden_truth.txt ./representation_files/weka_exp_0/train_subspaceRoot_weka_exp_0.arff ./train.arff 

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

echo train.arff has been generated  

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

#read -p "enter which chunk folder for the test-file : "  chunkname

declare -a arr=("chunk_1" "chunk1-2" "chunk1-2-3" "chunk1-2-3-4" "chunk1-2-3-4-5" "chunk1-2-3-4-5-6" "chunk1-2-3-4-5-6-7" "chunk1-2-3-4-5-6-7-8" "chunk1-2-3-4-5-6-7-8-9" "chunk1-2-3-4-5-6-7-8-9-10")

for chunkname in "${arr[@]}"
do
	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	echo deleting previous files in nltkdata test folders 
	find ./nltk_data/corpora/eRisk/test -maxdepth 2 -type f -delete 
	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

	echo now moving test files 
	python ./move-testfiles/generate_test_data.py ../development-dataset/ttdev-test ./nltk_data/corpora/eRisk/test "$chunkname"

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

	echo finished moving testfiles

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

	echo running featurespacetree train and test

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@  

	#python ./featurespacetree/entry_point.py pyramidal-soa2.yaml --train
	#python ./featurespacetree/entry_point.py pyramidal-soa2.yaml --test

	python ./featurespacetree/entry_point.py settings_soa_GOOD.yaml --train
	python ./featurespacetree/entry_point.py settings_soa_GOOD.yaml --test

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

	echo labeling the testing arff_file

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    python ./labeling/label_arff.py ./labeling/train_golden_truth.txt ./representation_files/weka_exp_0/test_subspaceRoot_weka_exp_0.arff ./test_"$chunkname".arff

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 

	echo test_"$chunkname".arff has been generated 

	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@     
done








  
