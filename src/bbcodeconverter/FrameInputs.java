package bbcodeconverter;
import javax.swing.*;
import java.awt.FlowLayout;

public class FrameInputs extends JFrame
{
	protected FrameInputs()
	{
		setTitle("BB-To-HTML Converter");
		setSize(600,400);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		setLocationRelativeTo(null); // Middle of screen
		
	    prepareComponents(); // Throws the assertion error
	    
	    setVisible(true); // This will paint the entire frame
	}
	private void prepareComponents()
	  {

	    assert SwingUtilities.isEventDispatchThread();
	    
		JLabel newLine;
	    JTextField inputFile = new JTextField(20);
	    FlowLayout header = new FlowLayout(FlowLayout.CENTER);
	    FlowLayout textInputField = new FlowLayout(FlowLayout.LEFT);
	    
	    setLayout(header);
	    add(new JLabel("Welcome to EoFF's BBCode Converter!"));
	    setLayout(textInputField);
	    add(inputFile);
	  }
	 
	  /**
	   * @param args not used
	   */
	  public static void main(String[] args)
	  {
	    SwingUtilities.invokeLater(new Runnable() {
	      @Override
	      public void run()
	      {
	    	  FrameInputs example = new FrameInputs();
	      }
	    });
	  }
}