import weka.core.Instances;
import weka.core.Instance;
import java.io.*;
import weka.core.converters.ArffLoader;
import weka.core.converters.ConverterUtils.DataSource;

public class CsvWriter{

	private String OutFile;

	public CsvWriter(String outFile){

		OutFile = outFile;
	}

	public void AppendToOutput(String subjectName,int decision,double delay){

		try{

			FileWriter MyFileWriter  = new FileWriter(OutFile,true);

			MyFileWriter.write(subjectName
								+ " "
								+ Integer.toString(decision)
								+" "
								+ Double.toString(delay)
								+"\n"
				);

			MyFileWriter.close();


		}
		catch(IOException ioe){

			ioe.printStackTrace();
		}
	}

	public void AppendToOutput(String subjectName,double decision,double delay){

		try{

			Double Prediction = decision;

			FileWriter MyFileWriter  = new FileWriter(OutFile,true);

			MyFileWriter.write(subjectName
								+ " "
								+ Integer.toString(Prediction.intValue())
								+" "
								+ Double.toString(delay)
								+"\n"
				);

			MyFileWriter.close();


		}
		catch(IOException ioe){

			ioe.printStackTrace();
		}
	}

	// for exhaustive results 
	public void AppendToOutput(String subjectName,double decision){

		try{

			Double Prediction = decision;

			FileWriter MyFileWriter  = new FileWriter(OutFile,true);

			MyFileWriter.write(subjectName
								+"	"
								+"	"
								+ Integer.toString(Prediction.intValue())
								+"\n"
				);

			MyFileWriter.close();


		}
		catch(IOException ioe){

			ioe.printStackTrace();
		}
	}

	/*public static void main(String[] args) {

		CsvWriter w = new CsvWriter("./pffft.txt");

		w.AppendToOutput("cmuk",0,0.6);
		w.AppendToOutput("eipku",1,2.9);
		
	} */
}