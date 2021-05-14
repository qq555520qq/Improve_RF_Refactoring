package robot_framework_refactor_tool.views;

import java.util.Arrays;

import org.eclipse.jface.dialogs.IDialogConstants;
import org.eclipse.jface.dialogs.IMessageProvider;
import org.eclipse.jface.dialogs.TitleAreaDialog;
import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.StyledText;
import org.eclipse.swt.custom.TableEditor;
import org.eclipse.swt.events.ModifyEvent;
import org.eclipse.swt.events.ModifyListener;
import org.eclipse.swt.events.MouseEvent;
import org.eclipse.swt.events.MouseListener;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.events.SelectionListener;
import org.eclipse.swt.graphics.Point;
import org.eclipse.swt.graphics.Rectangle;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.layout.RowLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Combo;
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

public class CreateANewKeyword extends TitleAreaDialog {
	private Table argumentTable;
	private TableEditor argumentEditor;
	private TableItem selectedArgument;
	private final String[] variableLabels = new String[] {"scalar($)", "list(@)","dict(&)"};
	private final String[] variableTypes = new String[] {"$", "@","&"};
	private StyledText keywordNameArea;
	private Label keywordNameLabel;
	private PyList newArguments;
	private String newKwName;
	public CreateANewKeyword(Shell parentShell, PyList arguments) {
		super(parentShell);
		this.newArguments = arguments;
	}

	@Override
	public void create() {
		super.create();
		setTitle("Add new keyword name and arguments");
        setMessage("Please click \"add\" button to add the argument and double click to edit the argument", IMessageProvider.INFORMATION);
	}

	private void createArguments(Composite container) {
        Label argumentLabel = new Label(container, SWT.NONE);
        argumentLabel.setText("Arguments");
        GridData argumentData = new GridData(385, 120);
        argumentData.grabExcessHorizontalSpace = true;
        argumentData.horizontalAlignment = GridData.FILL;
        argumentTable = new Table(container, SWT.MULTI | SWT.FULL_SELECTION);
        argumentEditor = new TableEditor(argumentTable);
        argumentEditor.horizontalAlignment = SWT.LEFT;
        argumentEditor.grabHorizontal = true;
        argumentTable.setHeaderVisible(true);
        argumentTable.setLinesVisible(true);
    	TableColumn argNameColumn = new TableColumn(argumentTable,SWT.LEFT);
    	argNameColumn.setWidth(200);
    	argNameColumn.setText("type");
    	TableColumn argTypeColumn = new TableColumn(argumentTable,SWT.LEFT);
    	argTypeColumn.setWidth(200);
    	argTypeColumn.setText("name");
    	argumentTable.setLayoutData(argumentData);
    	for(int index=0; index<this.newArguments.size();index++) {
    		this.newArguments.set(index, "$"+ ((String)this.newArguments.get(index)).substring(1));
    		new TableItem(argumentTable, SWT.LEFT).setText(new String[] {"$", ((String)this.newArguments.get(index)).substring(2, ((String)this.newArguments.get(index)).length()-1)});
    	}
    	argumentTable.addListener(SWT.MouseDown, e->{
			Point pt = new Point(e.x, e.y);
    		selectedArgument = argumentTable.getItem(pt);    		
    	});
    	argumentTable.addListener(SWT.MouseDoubleClick, e->{
				Point pt = new Point(e.x, e.y);
				selectedArgument = argumentTable.getItem(pt);
				if(selectedArgument==null)
					return;
				int selectedColumn = 0;
                for (int col = 0; col < argumentTable.getColumnCount(); col++) {
                    Rectangle rect = selectedArgument.getBounds(col);
                    if (rect.contains(pt)) 
                    	selectedColumn = col;
                }
                final int column = selectedColumn;
				Control editor = argumentEditor.getEditor();
				if(editor!=null)
					editor.dispose();
				Control tableEditor=null;
				if(column==1) {
					Text textEditor= new Text(argumentTable,SWT.None);
					String curText = selectedArgument.getText(column);
					textEditor.setText(curText);
					tableEditor = textEditor;
					textEditor.addModifyListener(event->{
						String argType = selectedArgument.getText(0);
						String argName = selectedArgument.getText(1);
						String originArg = argType+"{"+argName+"}";
						int index = newArguments.index(Py.newStringOrUnicode(originArg));
						String input = textEditor.getText();
						String newArg = argType+"{"+input+"}";
						selectedArgument.setText(column, input);
						newArguments.set(index, newArg);
					});
				}
				else {
					Combo comboEditor = new Combo(argumentTable, SWT.READ_ONLY);
					comboEditor.setItems(variableLabels);					
					String type = selectedArgument.getText(column);
					int typeIndex = Arrays.asList(variableTypes).indexOf(type);					
					String label = variableLabels[typeIndex];
					comboEditor.setText(label);
					tableEditor = comboEditor;
					comboEditor.addSelectionListener(new SelectionListener() {
						@Override
						public void widgetSelected(SelectionEvent e) {
							int selection = comboEditor.getSelectionIndex();
							String argType = selectedArgument.getText(0);
							String argName = selectedArgument.getText(1);
							String originArg = argType+"{"+argName+"}";
							int index = newArguments.index(Py.newStringOrUnicode(originArg));
							selectedArgument.setText(column, argType);
							String selectionType = variableTypes[selection];
							selectedArgument.setText(0, selectionType);
							comboEditor.dispose();
							newArguments.set(index, selectionType+"{"+argName+"}");
						}
						
						@Override
						public void widgetDefaultSelected(SelectionEvent e) {
							// TODO Auto-generated method stub
							
						}
					});
				}
				argumentEditor.setEditor(tableEditor, selectedArgument,column);
				tableEditor.forceFocus();
		});
    }

	private void createArgumentButtons(Composite container) {
		Composite buttons = new Composite(container, SWT.None);
    	buttons.setLayout(new RowLayout(SWT.None));
    	Button addArgument = new Button(buttons, SWT.LEFT);
    	addArgument.setSize(200, 200);
    	addArgument.setText("Add");
    	addArgument.addMouseListener(new MouseListener() {
			
			@Override
			public void mouseUp(MouseEvent e) {
				
			}
			
			@Override
			public void mouseDown(MouseEvent e) {
				int argumentLength = newArguments.size();
				String newArgument = "${argument"+String.valueOf(argumentLength+1)+"}";
				new TableItem(argumentTable, SWT.LEFT).setText(new String[] {newArgument.substring(0,1), newArgument.substring(2, newArgument.length()-1)});
				newArguments.append(Py.newStringOrUnicode(newArgument));
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
		});
    	Button removeArgument = new Button(buttons, SWT.LEFT);
    	removeArgument.setSize(200, 200);
    	removeArgument.setText("Remove");
    	removeArgument.addMouseListener(new MouseListener() {
			
			@Override
			public void mouseUp(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
			
			@Override
			public void mouseDown(MouseEvent e) {
				if(selectedArgument!=null && argumentTable.indexOf(selectedArgument)!=-1) {
					String argType = selectedArgument.getText(0);
					String argName = selectedArgument.getText(1);
					String argumentToRemove = argType+"{"+argName+"}";
					newArguments.remove(Py.newStringOrUnicode(argumentToRemove));
					argumentTable.remove(argumentTable.indexOf(selectedArgument));
				}
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
		});
    	
	}

    private void createKeywordNameArea(Composite container) {
    	keywordNameLabel = new Label(container, SWT.VIRTUAL);
    	keywordNameLabel.setText("New keyword name");
    	keywordNameLabel.setVisible(true);
    	keywordNameArea = new StyledText(container, SWT.BORDER);
    	GridData keywordNameGrid = new GridData();
    	keywordNameGrid.grabExcessHorizontalSpace = true;
    	keywordNameGrid.horizontalAlignment = GridData.FILL;
        keywordNameArea.setText("New Keyword");
        keywordNameArea.setLayoutData(keywordNameGrid);
        keywordNameArea.setEditable(true);
        keywordNameArea.setVisible(true);
        keywordNameArea.addModifyListener(new ModifyListener() {
			@Override
			public void modifyText(ModifyEvent e) {
				Button okButton = getButton(IDialogConstants.OK_ID);
				if (keywordNameArea.getText() == "") {
					okButton.setEnabled(false);
				}
				else {
					okButton.setEnabled(true);
				}
			}
        });
    }
	
	@Override
	protected Control createDialogArea(Composite parent) {
		Composite area = (Composite) super.createDialogArea(parent);
		Composite container = new Composite(area, SWT.NONE);
        container.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, true));
        GridLayout layout = new GridLayout(3, false);
        container.setLayout(layout);
		createArguments(container);
		createArgumentButtons(container);
		createKeywordNameArea(container);
		return area;
	}
	
	@Override
	protected void okPressed() {
		newKwName = keywordNameArea.getText();
		super.okPressed();
		
	}
	
	public String getNewKeywordName() {
		return newKwName;
	}


	@Override
	protected void configureShell(Shell newShell)
	{
	  super.configureShell(newShell);

	  newShell.setText("Step1: Create a new keyword");
	}
}
