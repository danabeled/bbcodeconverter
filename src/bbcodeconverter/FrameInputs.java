package bbcodeconverter;
import javax.swing.*;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;

public class FrameInputs extends JFrame
{
	protected static final String headerMessage = "Welcome to EoFF's BBCode Converter!";
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
	    // Set the layout flow
	    FlowLayout textInputField = new FlowLayout(FlowLayout.LEFT);
	    setLayout(textInputField);
	    
	    addHeaderPane();
	   
	  }
	private void addHeaderPane()
	{
		 //Create Header
	    JLabel header = new JLabel(headerMessage);
	    
		 //Create input file text fields
	    JTextField inputFile = new JTextField(20); 
	    
	    //Create Pane for file input
	    JPanel textPane = new JPanel();
	    
	    //Create Grid Layout
        GridBagLayout gridbag = new GridBagLayout();
        GridBagConstraints c = new GridBagConstraints();
        c.gridwidth = GridBagConstraints.REMAINDER; 
        c.anchor = GridBagConstraints.WEST;
        
        //Setup and add textPane
	    textPane.setLayout(gridbag);
	    textPane.add(header, c);
	    textPane.add(inputFile, c);
	    textPane.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));
	    add(textPane);
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