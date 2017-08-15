##############################################################################################
   I . HOW TO RUN EXPERIMENT
##############################################################################################

1) GO TO ERD SYSTEM FOLDER AND RUN RunExperiment.sh

2) IT REQUIRES PATH TO TRAINING ARFF FILE AND PATH TO FOLDER CONTAINING TEST FILES NAMED AS FOLLOWS

   test_chunk1.arff , test_chunk1-2.arff test_chunk1-2-3.arff and so on

   THERE ALREADY SUCH FOLDERS FOR EXAMPLE labeled_csa_arffs etc. 

   IF YOU WANT TO CREATE NEW ARFFS WITH NEW REPRESENTATION SEE NEXT SECTION OF THIS READ ME 

3) INPUT WHATEVER IS ASKED FOR BY THE SCRIPT 

4) IT WILL OUTPUT A TXT FILE NAMED BY YOU CONTAINING ALL REQUIRED RESULTS FSCORE,ERDE ETC.

###########################################################################################
  II . HOW TO GENERATE NEW REPRESENTATIONS (THAT IS INPUT FOR THE ABOVE )
###########################################################################################

1)  GO TO GENERATE INPUT FOLDER AND RUN generate-representation.sh 

    MAKE SURE YOU HAVE THE CORRECT REPRESENTATION SET IN settings_soa_GOOD.yaml , ( CSA etc.)

2) THE SCRIPT WILL FIRST GENERATE A LABELLED TRAIN FILE IN THE CURRENT DIRECTORY ( AS TRAIN FILES FOR THE SETTING WITH TVT f=4 ARE ALREADY PRESNET IN NLTK DATA)
   
   THEN ASK YOU FOR WHICH CHUNK YOU WANT TO GENERATE A TEST ARFF FILE FOR 

   YOU CAN ENTER THE FOLDER NAME FROM THE CLEANED_TESTING SUCH AS chunk_1 or chunk1-2-3-4-5 etc.

3) IT RANDOMIZES THE TEST FILES AND OUTPUTS A LABELLED TEST ARFF IN THE CURRENT DIRECTORY 

4) YOU CAN PUT THESE FILES IN ANY NEW FOLDER AND USE IT AS INPUT FOR THE ABOVE EXPERIMENT

NOTE : if you want to have tvt with different f value just delete train files in nltk data and move files as neccessary 

###############################################################################################################################

ADDITIONAL STUFF:

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  III.  HOW TO CREATE DEVLOPMENT SET FOR TUNING
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

1) GO TO DEVELOPMENT DATASET FOLDER DELETE OR MOVE DEV-TRAIN OR DEV-TEST FOLDERS IF ALREADY THERE OR JUST DELETE/MOVE THE FILES IN THEM

   AS THE SCRIPT WILL OUTPUT NEW FILES IN THESE FOLDERS

2) RUN devset-generator.py 

   Example  USAGE :   python devset-generator.py --path ../cleaned-dataset/cleaned-training --splitpercentage 70 --oversampling yes --fparam 4

3) THATS IT JUST BUILD ANY REPRESENTATION AS DESCRIBED IN II AND RUN EXPERIMENTS AS IN I.

$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
  IV. VISUALIZING REPRESENTATION ARFFS WITH TSNE 
$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

1) First run tsne_input.py example below
 
   python tsne_input.py ../erd-system/labeled_csa_arffs/training_csa.arff yes

   python tsne_input.py  < path to arff file >   < is it tvt or no tvt representation>

2) Then run tsne.py example below 

   python tsne.py --dim 6 --tvt yes

   python tsne.py --dim <number of initial dimensions> --tvt < tvt applied or not >

3) THATS IT YOU WILL SEE THE REQUIRED SCATTER PLOT 


