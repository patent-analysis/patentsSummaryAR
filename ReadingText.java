import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.PrintStream;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;


public class ReadingText {
	
	public static void main(String args[]) throws IOException {

		//Loading an existing document
		File file = new File("US8080243.pdf");
		PDDocument document = PDDocument.load(file);

		//Instantiate PDFTextStripper class
		PDFTextStripper pdfStripper = new PDFTextStripper();

		//Retrieving text from PDF document
		String text = pdfStripper.getText(document);
		
		PrintStream out = new PrintStream(new FileOutputStream("output.txt"));
		System.setOut(out);
		
		
		System.out.println(text);

		//Closing the document
		document.close();

	}
}
