import weka.core.Instance;
import weka.core.Instances;
import weka.core.converters.ArffLoader;
import weka.classifiers.bayes.NaiveBayesUpdateable;
import weka.classifiers.bayes.*;
import weka.core.Utils;
import weka.classifiers.*;
import java.util.*;
import java.io.*;

public class ClassifierBuilder{


	private NaiveBayesUpdateable NbClassifier;

	private Instances TrainingData;

	private ArffLoader DataLoader;

	private Classifier MyClassifier;

	private double PredictionThreshold;

	private int TrainingPercentage;

	public Instances DevTestSet;

	public ClassifierBuilder(String classifierName,Instances instances,int percentage){

		TrainingData = instances;

		TrainingPercentage = percentage;

		try{
		
			String [] NameAndOptions = Utils.splitOptions(classifierName);

			String ClassName = NameAndOptions[0];

			NameAndOptions[0]="";

			MyClassifier = (Classifier) Utils.forName(Classifier.class,ClassName,NameAndOptions);
		}
		catch(Exception excep){

			excep.printStackTrace();
		}
	
	}

	public ClassifierBuilder(String classifierName,Instances instances,int percentage,double threshold){

		TrainingData = instances;

		TrainingPercentage = percentage;

		PredictionThreshold = threshold;

		try{
		
			String [] NameAndOptions = Utils.splitOptions(classifierName);

			String ClassName = NameAndOptions[0];

			NameAndOptions[0]="";

			MyClassifier = (Classifier) Utils.forName(Classifier.class,ClassName,NameAndOptions);
		}
		catch(Exception excep){

			excep.printStackTrace();
		}
	
	}

	// in case of inceremental (or) Updateable classifier only 
	public ClassifierBuilder(Instances instances , ArffLoader loader) {

		TrainingData = instances;

		DataLoader = loader;

		NbClassifier = new NaiveBayesUpdateable();

	}

	private  int GetNumberOfInstances() throws IOException {

		int Count = 0;

		while(DataLoader.getNextInstance(TrainingData) != null){

			Count++;
		}		
 
		return Count;
	}


	public void TrainClassifier() throws Exception{

		if (TrainingPercentage == 100 ){

					MyClassifier.buildClassifier(TrainingData);
		}
		else{

			int SubSetSize = (int) Math.floor((TrainingData.numInstances()*TrainingPercentage)/100);

			int Total = TrainingData.numInstances();

			int Start = 0;

			try{
					
						Instances TrainingDataSubSet = new Instances(TrainingData,Start,SubSetSize);

						DevTestSet = new Instances(TrainingData,SubSetSize,Total - SubSetSize);

						MyClassifier.buildClassifier(TrainingDataSubSet);
					
			}
			catch(IllegalArgumentException iae){

				iae.printStackTrace();
			}
	    }

	}

	// this method is only valid to train classifiers implementing the 'Updateable' interface

	public void TrainClassifierIncremental(int percentage) throws Exception{


		NbClassifier.buildClassifier(TrainingData);

		int Stop = (int) Math.floor((GetNumberOfInstances()*percentage)/100);

		int Start = 0;

		Instance Current;

		while(((Current = DataLoader.getNextInstance(TrainingData)) != null) && (Start<=Stop)){

				NbClassifier.updateClassifier(Current);
			    Start++;
		}
	
	} 

	public void PrintClassifier(){

		System.out.println(MyClassifier);
	}

	public void EvaluateAgainstTestSet(Instances testData) throws Exception{

		

		Evaluation Eval = new Evaluation(testData);

		/*double [] Predictions = MyClassifier.distributionForInstance(TestData.get(2));

		for(int Index = 0; Index < Predictions.length; Index++ ){

			System.out.println("Probability of class "+
				                TestData.classAttribute().value(Index)+
				                ": "+
				                 Double.toString(Predictions[Index]));
		} */

		Eval.evaluateModel(MyClassifier,testData);

		System.out.println(Eval.toSummaryString());

		System.out.println(Eval.toClassDetailsString());

		System.out.println("#############################################");

	}

	public void EvaluateAgainstTestSet(Instances testData,int whichChunk) throws Exception{

		

		Evaluation Eval = new Evaluation(testData);

		double [] Predictions = MyClassifier.distributionForInstance(testData.get(2));

		for(int Index = 0; Index < Predictions.length; Index++ ){

			System.out.println("Probability of class "+
				                testData.classAttribute().value(Index)+
				                ": "+
				                 Double.toString(Predictions[Index]));
		} 

		Eval.evaluateModel(MyClassifier,testData);

		System.out.println(Eval.toSummaryString());

		System.out.println(Eval.toClassDetailsString());

		System.out.println("######################"+"upto chunk: "+whichChunk+"#######################");

	}

	// Policy function to decide when predcition is good enough as final prediction
	private boolean Policy(double probability){

		if(probability >= PredictionThreshold ){
			return true;
		}
		else {
			return false;
		}

	}

	private boolean PolicyWithDiff(double probability){

		if(Math.abs(probability - PredictionThreshold ) >= 0.1){
			return true;
		}
		else {
			return false;
		}

	}

	// for now a dummy delay function 
	private double CalculateDelay(){

		return 0;
	}

	
	public void RunEarlyRiskClassificationChunkByChunk(ChunkManager manager,int howManyChunks,int uptoThisChunk) throws Exception{


		for(int OuterIndex=1; OuterIndex<=howManyChunks; OuterIndex++){

			manager.GoToNextChunk(OuterIndex);

			List<String> SubjectNames = manager.GetSubjectsForCurrentChunk();

			Instances TestData = manager.GetDataFromCurrentChunk();

			// Get console output for no policy #weka metrics 
			EvaluateAgainstTestSet(TestData,OuterIndex);

			CsvWriter Writer = new CsvWriter("./ritual_"+Integer.toString(OuterIndex)+".txt");

			for(int InnerIndex =0; InnerIndex < TestData.numInstances(); InnerIndex++ ){

				double [] Predictions = MyClassifier.distributionForInstance(TestData.get(InnerIndex));

				if (OuterIndex == uptoThisChunk){

				Writer.AppendToOutput(SubjectNames.get(InnerIndex),MyClassifier.classifyInstance(TestData.get(InnerIndex)));
					boolean Written = false;

					if(Predictions[1] > Predictions[0]){

						if(Policy(Predictions[1])){

							Writer.AppendToOutput(SubjectNames.get(InnerIndex),1);
							Written = true;
						}
					}else if (Predictions[0] > Predictions[1]) {

						if(Policy(Predictions[0])){

							Writer.AppendToOutput(SubjectNames.get(InnerIndex),2);
							Written = true;
					   }
					}
					if(!Written)
					{ 
							Writer.AppendToOutput(SubjectNames.get(InnerIndex),0);
					} 
				}
				else {
					Writer.AppendToOutput(SubjectNames.get(InnerIndex),0);
				} 	
			}
		}	
	

	}

	public void RunEarlyRiskClassificationChunkByChunkNoPolicy(ChunkManager manager,int howManyChunks) throws Exception{

		for(int OuterIndex=1; OuterIndex<=howManyChunks; OuterIndex++){

			manager.GoToNextChunk(OuterIndex);

			List<String> SubjectNames = manager.GetSubjectsForCurrentChunk();

			Instances TestData = manager.GetDataFromCurrentChunk();

			CsvWriter Writer = new CsvWriter("./output_for_chunk"+Integer.toString(OuterIndex)+".txt");

			for(int InnerIndex =0; InnerIndex < TestData.numInstances(); InnerIndex++ ){

					Writer.AppendToOutput(SubjectNames.get(InnerIndex),
						MyClassifier.classifyInstance(TestData.get(InnerIndex)),
						CalculateDelay());
			}

		}

	} 
	

	
	public void RunEarlyRiskClassificationExhaustive(ChunkManager manager,int howManyChunks) throws Exception{

	/*	get chunks iteratively

		for each chunk iterate over the instances
		
		classify each instance if policy approves output

		it to the file in required format using CsvWriter 

		if all chunks are used and there are still remaining subjects

		output them as negative class */

		String positiveSubject = "test_subject3112";

		String negativeSubject = "test_subject5489";

		for(int OuterIndex=1; OuterIndex<=howManyChunks; OuterIndex++){

			manager.GoToNextChunk(OuterIndex);

			List<String> SubjectNames = manager.GetSubjectsForCurrentChunk();

			Instances TestData = manager.GetDataFromCurrentChunk();

			// Get console output for no policy #weka metrics 
			//EvaluateAgainstTestSet(TestData,OuterIndex);

			CsvWriter Writer = new CsvWriter("./ritual_"+Integer.toString(OuterIndex)+".txt");

			for(int InnerIndex =0; InnerIndex < TestData.numInstances(); InnerIndex++ ){

				double [] Predictions = MyClassifier.distributionForInstance(TestData.get(InnerIndex));


					boolean Written = false;

					/*if(positiveSubject.equals(SubjectNames.get(InnerIndex)))
					{
						System.out.println("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
						System.out.println("positive subject ");
						System.out.println(Predictions[1]);
						System.out.println("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
					}
					if(negativeSubject.equals(SubjectNames.get(InnerIndex)))
					{
						System.out.println("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
						System.out.println("negative subject ");
						System.out.println(Predictions[1]);
						System.out.println("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@");
					}*/

					if(Predictions[1] > Predictions[0]){

						if(Policy(Predictions[1])){

							Writer.AppendToOutput(SubjectNames.get(InnerIndex),1);
							Written = true;
						}
					}else if (Predictions[0] > Predictions[1]) {

						if(Policy(Predictions[0])){

							Writer.AppendToOutput(SubjectNames.get(InnerIndex),2);
							Written = true;
					   }
					}
					if(!Written)
					{ 
							Writer.AppendToOutput(SubjectNames.get(InnerIndex),0);
					} 


			}

		}

	}
	
/*
	Experimental do not use 

	public void RunEarlyRiskClassificationExhaustiveWithCache(ChunkManager manager,int howManyChunks) throws Exception{

		HashMap <String,Integer> Cache = new HashMap <String,Integer> ();

		for(int OuterIndex=1; OuterIndex<=howManyChunks; OuterIndex++){

			manager.GoToNextChunk(OuterIndex);

			List<String> SubjectNames = manager.GetSubjectsForCurrentChunk();

			Instances TestData = manager.GetDataFromCurrentChunk();

			// Get console output for no policy #weka metrics 
			//EvaluateAgainstTestSet(TestData,OuterIndex);

			CsvWriter Writer = new CsvWriter("./ritual_"+Integer.toString(OuterIndex)+".txt");

			for(int InnerIndex =0; InnerIndex < TestData.numInstances(); InnerIndex++ ){

				double [] Predictions = MyClassifier.distributionForInstance(TestData.get(InnerIndex));

				Double Prediction = MyClassifier.classifyInstance(TestData.get(InnerIndex));


		
//					Writer.AppendToOutput(SubjectNames.get(InnerIndex),0); 
				


			}

		}

	} */

}