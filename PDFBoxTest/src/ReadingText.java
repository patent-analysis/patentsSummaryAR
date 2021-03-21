import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;


public class ReadingText {
	
	public static void main(String args[]) throws IOException {
		
		//Directory for PDF and txt files
		File dirTxt = new File("PatentsTxt");
		File dirPDF = new File("PatentsPDF");
		
		//Loop through PDF directory
		File[] directoryListing = dirPDF.listFiles();
		if (directoryListing != null) {
			for (File pdfFile : directoryListing) {
				
				String pdfFileName = pdfFile.getName();
				
				//Loading an existing document
				String inputPDF = dirPDF + "/" + pdfFileName;
				File file = new File(inputPDF);
				PDDocument document = PDDocument.load(file);
				
				//Instantiate PDFTextStripper class
				PDFTextStripper pdfStripper = new PDFTextStripper();
				
				//Retrieving text from PDF document
				String text = pdfStripper.getText(document);
				
				//Set output to a file
				String outputTxt = dirTxt + "/" + pdfFileName + ".txt";
				
				PrintStream out = new PrintStream(new FileOutputStream(outputTxt));
				System.setOut(out);
				
				//Print to a file
				System.out.println(text);
                
				//Closing the document
				document.close();
			}
		}
	}
}
