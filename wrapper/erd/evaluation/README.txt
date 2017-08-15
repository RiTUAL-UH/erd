ERISK 2017: EARLY RISK PREDICTION ON THE INTERNET: EXPERIMENTAL FOUNDATIONS
===========================================================================

Pilot task on Early Detection of Depression: 

This is an exploratory task on early risk detection of depression. The challenge consists of sequentially processing pieces of evidence and detect early traces of depression as soon as possible. 
The task is mainly concerned about evaluating Text Mining solutions and, thus, it concentrates on texts written in Social Media. Texts should be processed in the order they were created. 
In this way, systems that effectively perform this task could be applied to sequentially monitor user interactions in blogs, social networks, or other types of online media.

The test collection for this pilot task is the collection described in [Losada & Crestani 2016]. It is a collection of writings (posts or comments) from a set of Social Media users. 
There are two categories of users, depressed and non-depressed, and, for each user, the collection contains a sequence of writings (in chronological order). For each user, his collection 
of writings has been divided into 10 chunks. The first chunk contains the oldest 10% of the messages, the second chunk contains the second oldest 10%, and so forth.

The task is organized into two different stages:

* Training stage. Initially, the teams that participate in this task will have access to a training stage where we will release the whole history of writings for a set of training users 
(we will provide all chunks of all training users), and we will indicate what users have explicitly mentioned that they have been diagnosed with depression. The participants can therefore 
tune their systems with the training data.

* Test stage. The test stage will consist of 10 sequential releases of data (i.e. done at different dates). The first release will consist of the 1st chunk of data (oldest writings of all 
test users), the second release will consist of the 2nd chunk of data (second oldest writings of all test users), and so forth. After each release, the participants will have a few days 
to process the data and, before the next release, each participating system has to choose between two options: a) emitting a decision on the user (i.e. depressed or non-depressed), 
or b) seeing more chunks. This choice has to be made for each user in the collection. If the system emits a decision, its decision will be final and it will be evaluated based 
on the correctness of the system's decision and the number of chunks required to make the decision (using a metric for which the fewer writings required to make the alert, the better). 
If the system does not emit a decision then it will have access to the next chunk of data, that is it will have access to more writings, but it will have a penalty for a “later emission”).

This folder contains the training data:

- risk_golden_truth.txt: this file contains the ground truth (one line per subject). The code 1 means that the subject is a risk case of depression, while 0 means that the subject is a non-risk case.
- positive_examples_anonymous_chunks: this folder, which stores all the posts of the risk cases, contains 10 subfolders. Each subfolder corresponds with one chunk. Chunk 1 contains the oldest
writings of all users (first 10% of submitted posts or comments), chunk 2 contains the second oldest writings, and so forth. The name of the files follows de convention: <subjectname>_<chunknumber>.xml .
- negative_examples_anonymous_chunks: this folder, which stores all the posts of the non-risk cases, contains 10 subfolders. Each subfolder corresponds with one chunk. Chunk 1 contains the oldest
writings of all users (first 10% of submitted posts or comments), chunk 2 contains the second oldest writings, and so forth. The name of the files follows de convention: <subjectname>_<chunknumber>.xml .
- scripts evaluation (see below)

This is the training data and, therefore, you get all chunks now. But you should adapt your algorithms in a way that the chunks are processed according to the sequence (for example, don't process chunk3 if you
have not processed chunk1 and chunk2). 

IMPORTANT INFORMATION ABOUT THE TEST STAGE:

At test time, we will first release chunk1 for the test subjects and ask you for your output. A few days later, we will release chunk2, and so forth. 
The format required for the output file to be sent after each release of test data will be the following:

2-column text file. The name of the file should be ORG_n.txt  (where ORG is an acronym for your organization and n is the chunk number; e.g.    usc_1.txt)

The file should contain one line per user in the test collection:

test_subject_id1		CODE
test_subject_id2		CODE
......

NOTE: put exactly two tabs between the subject name and the CODE (aggregate_results.py assumes that the files have this format)

test_subject_idn is the id of the test_subject (ID field in the XML files)
CODE is your decision about the subject: three possible values......  0 means that you don't want to emit a decision on this subject (you want to wait and see more evidence)
																	  1 means that you want to emit a decision on this subject, and your decision is that he/she is a risk case of depression
																	  2 means that you want to emit a decision on this subject, and your decision is that he/she is NOT a risk case of depression

if you emit a decision on a subject then any future decision on the same subject will be ignored. 
for simplicity, you can include all subjects in all your submitted files but, for each user, your algorithm will be evaluated based on the first file that contains a decision on the subject. 
and you cannot say 0 all the time: at some point you need to make a decision on every subject (i.e. at the latest, after the 10th chunk,
you need to emit your decision). 																  
																	  
if a team does not submit the required file before the deadline then we'll take the previous file from the same team and assume that all things stay the same (no new emissions for this round).
if a team does not submit the file after the first round then we´ll assume that the team does not take any decision (all subjects set to 0 -no decision- ). 

SCRIPTS FOR EVALUATION:

To facilitate your experiments, we provide two scripts that could be of help during the training stage. These scripts are in the scripts evaluation folder. We recommend you to follow these steps:

1) use your early detection algorithm to process chunk1 files and produce your first output file (e.g. usc_1.txt). This file follows the format described above (0/1/2 for each subject).
Do the same for all the chunki files (i: 2, ..., 10). When you process chunki files it is OK to use information from chunkj files (for j<=i). Note that the chunkj files (such that j=1...i) contain all 
posts/comments that you have seen after the ith release of data. 

2) you now have your 10 output files (e.g. usc_1.txt ... usc_10.txt). as argued above, you need to take a decision on every subject 
(you cannot say 0 all the time). so, every subject needs to have 1/2 assigned in some of your output files. 

use the aggregate_results.py to combine your output files into a global output file. This aggregation script has two inputs: 1) the folder where you have your 10 output files
and 2) the path to the file writings_per_subject_all_train.txt. The writings_per_subject_all_train.txt file stores the number of writings per subject. 
This is required because we need to know how many writings where needed to take each decision. For instance, if subject_k has a total number of 500 writings in the collection 
then every chunk has 50 writings from subject_k. If your team needed 2 chunks to make a decision on subject_k then we will store 100 as number of writings that you needed to take this decision.

Example of usage:  $ python aggregate_results.py -path <path to the folder where you have your 10 files> -wsource <path to the writings_per_subject_all_train.txt file>

This scripts creates a file, e.g. usc_global.txt, which stores your final decision on every subject and the number of writings that you saw before making the decision.

3) get the final performance results from the erisk_eval.py script. It has three inputs: a) path to the golden truth file (risk_golden_truth.txt), b) path to the overall output file, and 
c) value of o (delay parameter of the ERDE metric). 

Example: $ python erisk_eval.py -gpath <path to the risk_golden_truth.txt file> -ppath <path to the overall output file> -o <value of ERDE delay parameter>
Example: $ python erisk_eval.py -gpath ../risk_golden_truth.txt -ppath ../folder/usc_global.txt -o 5


References:

[Losada & Crestani 2016] David E. Losada, Fabio Crestani. A Test Collection for Research on Depression and Language use. 7th Conference Labs of the Evaluation Forum, CLEF 2016, Évora (Portugal), 2016