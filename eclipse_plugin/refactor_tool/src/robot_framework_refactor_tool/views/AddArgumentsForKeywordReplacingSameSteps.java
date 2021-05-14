package robot_framework_refactor_tool.views;


import org.eclipse.jface.dialogs.IDialogConstants;
import org.eclipse.jface.dialogs.IMessageProvider;
import org.eclipse.jface.dialogs.TitleAreaDialog;
import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.StyledText;
import org.eclipse.swt.custom.TableEditor;
import org.eclipse.swt.events.MouseEvent;
import org.eclipse.swt.events.MouseListener;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.layout.RowLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Table;
import org.eclipse.swt.widgets.TableColumn;
import org.eclipse.swt.widgets.TableItem;
import org.eclipse.swt.widgets.Text;
import org.python.core.Py;
import org.python.core.PyList;

import helper.NewRefactorHelper;

public class AddArgumentsForKeywordReplacingSameSteps extends TitleAreaDialog {
	private Table argumentTable;
	private TableEditor argumentEditor;
	private TableItem selectedArgument;
	private NewRefactorHelper helper;
	private StyledText previewArea;
	private Label previewLabel;
	private PyList newArguments;
	private PyList sameStepsBlock;
	private PyList argumentsOfReplacedKeyword;
	public AddArgumentsForKeywordReplacingSameSteps(Shell parentShell, NewRefactorHelper helper, PyList sameStepsBlock, PyList arguments, PyList argumentsOfReplacedKeyword) {
		super(parentShell);
		this.argumentsOfReplacedKeyword = argumentsOfReplacedKeyword;
		this.newArguments = arguments;
		this.helper = helper;
		this.sameStepsBlock = sameStepsBlock;
	}

	public AddArgumentsForKeywordReplacingSameSteps(Shell parentShell, NewRefactorHelper helper, PyList sameStepsBlock) {
		super(parentShell);
		this.helper = helper;
		this.sameStepsBlock = sameStepsBlock;
	}

	@Override
	public void create() {
		super.create();
		if(this.newArguments != null) {
			setTitle("Add arguments for the keyword that will replace same steps");
			setMessage("Please click add button to add data and double click to edit data", IMessageProvider.INFORMATION);
		}
		else {
			setTitle("Present same steps block");	
	        setMessage("Please check are the steps that you want", IMessageProvider.INFORMATION);
		}
        Button cancelButton= getButton(IDialogConstants.CANCEL_ID);
    	cancelButton.setVisible(false);
	}

	private void createArguments(Composite container) {
        Label argumentLabel = new Label(container, SWT.NONE);
        argumentLabel.setText("Arguments");
        GridData argumentData = new GridData(0, 120);
        argumentData.grabExcessHorizontalSpace = true;
        argumentData.horizontalAlignment = GridData.FILL;
        argumentTable = new Table(container, SWT.MULTI | SWT.FULL_SELECTION);
        argumentEditor = new TableEditor(argumentTable);
        argumentEditor.horizontalAlignment = SWT.LEFT;
        argumentEditor.grabHorizontal = true;
        argumentTable.setHeaderVisible(true);
        argumentTable.setLinesVisible(true);
    	TableColumn argColumn = new TableColumn(argumentTable,SWT.LEFT);
    	argColumn.setWidth(315);
    	argColumn.setText("arguments");
    	argumentTable.setLayoutData(argumentData);
    	argumentTable.addListener(SWT.MouseDown, e->{
			Point pt = new Point(e.x, e.y);
    		selectedArgument = argumentTable.getItem(pt);
    		Control editor = argumentEditor.getEditor();
			if(editor!=null)
				editor.dispose();
    	});
    	argumentTable.addListener(SWT.MouseDoubleClick, e->{
			Point pt = new Point(e.x, e.y);
			selectedArgument = argumentTable.getItem(pt);
			if(selectedArgument==null) 
				return;
			Control editor = argumentEditor.getEditor();
			if(editor!=null)
				editor.dispose();
			Control tableEditor=null;
			Text textEditor= new Text(argumentTable,SWT.None);
			String curText = selectedArgument.getText(0);
			textEditor.setText(curText);
			tableEditor = textEditor;
			textEditor.addModifyListener(event->{
				String originArg = selectedArgument.getText(0);
				int index = newArguments.index(Py.newStringOrUnicode(originArg));
				String input = textEditor.getText();
				selectedArgument.setText(0, input);
				newArguments.set(index, input);
			});
			argumentEditor.setEditor(tableEditor, selectedArgument, 0);
			tableEditor.forceFocus();
		});
    }

	private void createArgumentButtons(Composite container) {
		Composite buttons = new Composite(container, SWT.None);
    	buttons.setLayout(new RowLayout(SWT.None));
    	Button addArgument = new Button(buttons, SWT.LEFT);
    	if(argumentsOfReplacedKeyword.size() == 0) {
			addArgument.setEnabled(false);
		}
    	addArgument.setSize(200, 200);
    	addArgument.setText("Add");
    	addArgument.addMouseListener(new MouseListener() {
			
			@Override
			public void mouseUp(MouseEvent e) {
				
			}
			
			@Override
			public void mouseDown(MouseEvent e) {
				int argumentLength = newArguments.size();
				String newArgument = "argument"+String.valueOf(argumentLength+1);
				new TableItem(argumentTable, SWT.LEFT).setText(new String[] {newArgument});
				newArguments.append(Py.newStringOrUnicode(newArgument));
				if(newArguments.size() == argumentsOfReplacedKeyword.size()) {
					addArgument.setEnabled(false);
				}
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
		});
    	Button removeArgument = new Button(buttons, SWT.LEFT);
    	removeArgument.setSize(200, 200);
    	removeArgument.setText("Remove");
    	if(argumentsOfReplacedKeyword.size() == 0) {
			addArgument.setEnabled(false);
		}
    	removeArgument.addMouseListener(new MouseListener() {
			
			@Override
			public void mouseUp(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
			
			@Override
			public void mouseDown(MouseEvent e) {
				if(selectedArgument!=null && argumentTable.indexOf(selectedArgument)!=-1) {
					String argumentToRemove = selectedArgument.getText(0);
					newArguments.remove(Py.newStringOrUnicode(argumentToRemove));
					argumentTable.remove(argumentTable.indexOf(selectedArgument));
					if(newArguments.size() != argumentsOfReplacedKeyword.size()) {
						addArgument.setEnabled(true);
					}
				}
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
		});
    	
	}
    
    private void createPreviewArea(Composite container) {
    	previewLabel = new Label(container, SWT.VIRTUAL);
    	previewLabel.setText("Present same steps");
    	previewLabel.setVisible(true);
    	previewArea = new StyledText(container, SWT.BORDER);
    	GridData previewGrid = new GridData();
        previewGrid.grabExcessHorizontalSpace = true;
        previewGrid.horizontalAlignment = GridData.FILL;
        previewArea.setText(helper.presentSameSteps(sameStepsBlock));
        previewArea.setLayoutData(previewGrid);
        previewArea.setEditable(false);
        previewArea.setVisible(true);
    }
	
	@Override
	protected Control createDialogArea(Composite parent) {
		Composite area = (Composite) super.createDialogArea(parent);
		Composite container = new Composite(area, SWT.NONE);
        container.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, true));
        GridLayout layout = new GridLayout(3, false);
        container.setLayout(layout);
        if(this.newArguments != null) {
        	createArguments(container);
        	createArgumentButtons(container);
        }
		createPreviewArea(container);
		return area;
	}
	
	@Override
	protected void okPressed() {
		super.okPressed();
		
	}

	@Override
	protected void configureShell(Shell newShell)
	{
	  super.configureShell(newShell);

	  newShell.setText("Step2: Replace the same steps with new keyword");
	}

}
