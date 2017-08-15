#!/bin/bash

export CLASSPATH=../weka-3-8-1/weka.jar:$CLASSPATH

read -p "enter path to training arff file"  trainpath

read -p "enter path to test files folder"  testpath

java Main $trainpath $testpath

read -p "enter name for output folder"  foldername

mkdir ../evaluation/$foldername

mv ritual_*.txt ../evaluation/$foldername

echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

echo begining erisk evaluation 

read -p "was the experiment run on test set (yes) or development set(no) ? " response 

if [ $response = "yes" ]
then 
	python ../evaluation/aggregate_results.py -path ../evaluation/$foldername -wsource ../evaluation/writings_all_test_users.txt
	read -p "enter the erde delay parameter o (type 5 or 50) ?" oparam
	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	read -p "enter output file name (no file extension)?" outfile
	python ../evaluation/erisk_eval.py -gpath ../evaluation/test_golden_truth.txt -ppath ../evaluation/$foldername/ritual_global.txt -o $oparam #> $outfile.txt
	python ../evaluation/erisk_eval.py -gpath ../evaluation/test_golden_truth.txt -ppath ../evaluation/$foldername/ritual_global.txt -o 50
else
    python ../evaluation/aggregate_results.py -path ../evaluation/$foldername -wsource ../evaluation/dev-writings.txt
	read -p "enter the erde delay parameter o (type 5 or 50) ?" oparam  
	echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	read -p "enter output file name (no file extension)?" outfile
	python ../evaluation/erisk_eval.py -gpath ../evaluation/dev-truth.txt -ppath ../evaluation/$foldername/ritual_global.txt -o $oparam > $outfile.txt 
fi
echo "output file generated in current directory"

