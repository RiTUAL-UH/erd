import weka.core.Instances;
import weka.core.Instance;
import java.io.*;
import weka.core.converters.ArffLoader;
import weka.core.converters.ConverterUtils.DataSource;
import java.util.*;

public class ChunkManager{

	private String TestDataFolder;

	private List<String> Subjects;

	private static final String FileBaseName = "test_chunk";

	private String CurrentChunk;

	private ArffReader MyArffReader;


	public ChunkManager (String testDataFolder){

		TestDataFolder = testDataFolder;

		Subjects = new ArrayList<String> ();

		CurrentChunk = FileBaseName;

		MyArffReader = new ArffReader();

	}

	public void GoToNextChunk(int index){

		if(index > 1){

			CurrentChunk+= "-"+ Integer.toString(index);
		}
		else if(index == 1){

			CurrentChunk+=Integer.toString(index);
		}
	}

	//  subjects are not in same order in all chunks 
	public List<String> GetSubjectsForCurrentChunk(){

	try (BufferedReader BuffReader = new BufferedReader(new FileReader(TestDataFolder+"/"+CurrentChunk+".arff"))) {

	    String Line;

	    while ((Line = BuffReader.readLine()) != null) {

	    	if(Line.charAt(0) != '@'){

	    		String [] SpaceSplitted = Line.split(" ");

	    		String ToSplitFurther = SpaceSplitted[SpaceSplitted.length-1];

	    		String [] UnderScoreSplitted = ToSplitFurther.split("_");

	    		for(String x: UnderScoreSplitted){

	    			if(x.length() > 6 && x.substring(0,7).equals("subject")){

	    				// Subjects.add("test_"+x);
	    				Subjects.add("test_subject"+x.substring(7,x.length()));

	    			}
	    		}
	    	}

	    }
	}
	catch(IOException ioe){

		ioe.printStackTrace();
	}

		return Subjects;

	}

	public Instances GetDataFromCurrentChunk() throws Exception {

		return MyArffReader.GetAllTestData(TestDataFolder+"/"+CurrentChunk+".arff");

	}


/*	 public static void main(String[] args) {

		try{

			ChunkManager cm = new ChunkManager("./labeled_csa_arffs");

			for(int i=1; i<=10; i++){

				cm.GoToNextChunk(i);

				for( String s : cm.GetSubjectsForCurrentChunk()){

					System.out.println(s);
				}

				System.out.println("################################# "+i);

			}

		}
		catch(Exception e){

			e.printStackTrace();
		}
		
	} */

}
