package bbcodeconverter;
import javax.swing.*;
import javax.swing.filechooser.FileNameExtensionFilter;

import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;

public class FrameInputs extends JFrame
{
	protected static final String headerMessage = "Welcome to EoFF's BBCode to HTML Converter "; 
	protected static final String fileMessage = "Please select a filepath: ";
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
		// Create Total GUI Panel
		JPanel totalPanel = new JPanel();
		// Create Header Panel
		JPanel headerPanel = new JPanel();
		headerPanel.setLocation(100,0);
		headerPanel.setSize(300,300);
		totalPanel.add(headerPanel);
		
		// Create Header Text
		JLabel headerLabel = new JLabel(headerMessage);
		headerLabel.setLocation(0,0);
		headerLabel.setHorizontalAlignment(0);
		totalPanel.add(headerLabel);
	    
		 //Create Input Label
	    JLabel fileLabel = new JLabel(fileMessage);
	    fileLabel.setLocation(400,200);
	    fileLabel.setHorizontalAlignment(0);
	    totalPanel.add(fileLabel);
	    
		 //Create input file text fields
	    JTextField inputFile = new JTextField(20); 

		
	    //Create Grid Layout
        //GridBagLayout gridbag = new GridBagLayout();
        //GridBagConstraints c = new GridBagConstraints();
        //c.gridwidth = GridBagConstraints.CENTER; 
        //c.anchor = GridBagConstraints.WEST;
        
        //Create File Opener Button
        //JButton fileChooseButton = new JButton("...");
        
        //Setup and add textPane
	    //inputPanel.add(fileLabel);
	    //inputPanel.add(inputFile);
	    //inputPanel.add(fileChooseButton);
	    //add(headerLabel);
	    //add(inputPane);
	    
		setContentPane(totalPanel);
	}
	public static void openFileChooserPopUp()
	{
		JFileChooser chooser = new JFileChooser();
        FileNameExtensionFilter filter = new FileNameExtensionFilter(
            "Text Files", "txt");
        chooser.setFileFilter(filter);
        int returnVal = chooser.showOpenDialog(getParent());
        if(returnVal == JFileChooser.APPROVE_OPTION) {
           System.out.println("You chose to open this file: " +
                chooser.getSelectedFile().getName());
        }
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