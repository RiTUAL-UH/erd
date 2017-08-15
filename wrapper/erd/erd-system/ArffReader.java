import weka.core.Instances;
import weka.core.Instance;
import java.io.*;
import weka.core.converters.ArffLoader;
import weka.core.converters.ConverterUtils.DataSource;

public class ArffReader {

	//private String PathToTrain;

	//private String PathToTest;

	private ArffLoader Loader;


/*	public ArffReader (String trainPath , String testPath){

		PathToTrain = trainPath;

		PathToTest = testPath;
	} */

/*	public ArffReader (String testPath){

		PathToTrain = "";

		PathToTest = testPath;

	} */

	public ArffReader(){}

	public Instances GetTrainingData (String pathToTrain) throws Exception {

			DataSource Source = new DataSource(pathToTrain);

			Instances Data = Source.getDataSet();

			Data.setClassIndex(Data.numAttributes()-1);

			return Data;

	}

	public Instances GetTrainingData (String pathToTrain,int classIndex) throws Exception {

			DataSource Source = new DataSource(pathToTrain);

			Instances Data = Source.getDataSet();

			Data.setClassIndex(classIndex);

			return Data;

	}


	public Instances GetTrainingDataIncremental (String pathToTrain) throws IOException, FileNotFoundException{

			Loader = new ArffLoader();

			Loader.setFile( new File(pathToTrain) );

			Instances Data = Loader.getStructure();

			Data.setClassIndex(Data.numAttributes()-1);

			return Data;

	}


	public Instances GetTrainingDataIncremental (String pathToTrain,int classIndex) throws IOException, FileNotFoundException{


			Loader = new ArffLoader();
			
			Loader.setFile(new File(pathToTrain));

			Instances Data = Loader.getStructure();

			Data.setClassIndex(classIndex);

			return Data;
	}

	public ArffLoader GetLoader(){

		return Loader;
	}

	// Do class attribute and it's associated values be chucked off in test data before this ?
	public Instances GetAllTestData (String pathToTest) throws Exception {

		DataSource Source = new DataSource(pathToTest);

		Instances Data = Source.getDataSet();

		Data.setClassIndex(Data.numAttributes()-1);

		return Data;		

	/*	BufferedReader BReader = new BufferedReader(
							     new FileReader(PathToTest)
			                     );

		Instances Data = new Instances(BReader);

		BReader.close();

		Data.setClassIndex(Data.numAttributes()-1);

		return Data; */
	} 

	public Instances GetAllTestData (String pathToTest,int classIndex) throws Exception {

		DataSource Source = new DataSource(pathToTest);

		Instances Data = Source.getDataSet();

		Data.setClassIndex(classIndex);

		return Data;		

	}
	
}