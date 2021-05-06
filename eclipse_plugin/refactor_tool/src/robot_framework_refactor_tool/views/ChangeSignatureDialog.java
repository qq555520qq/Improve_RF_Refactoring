package robot_framework_refactor_tool.views;

import java.util.Arrays;
import org.eclipse.jface.dialogs.IMessageProvider;
import org.eclipse.jface.dialogs.TitleAreaDialog;
import org.eclipse.swt.SWT;
import org.eclipse.swt.custom.StyledText;
import org.eclipse.swt.custom.TableEditor;
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
import org.python.core.PyObject;

import helper.RefactorHelper;

public class ChangeSignatureDialog extends TitleAreaDialog {
	private Table argumentTable;
	private Table returnTable;
	private TableEditor argumentEditor;
	private TableEditor returnEditor;
	private TableItem selectedArgument;
	private TableItem selectedReturn;
	private StyledText previewArea;
	private Label previewLabel;
	private boolean isPreview=false;
	private PyObject keyword;
	private RefactorHelper helper;
	private PyObject argumentObj;
	private PyObject returnObj;
	private final String[] variableLabels = new String[] {"scalar($)", "list(@)","dict(&)"};
	private final String[] variableTypes = new String[] {"$", "@","&"};
	public ChangeSignatureDialog(Shell parentShell, RefactorHelper helper,PyObject keyword) {
		super(parentShell);
		this.keyword = keyword;
		this.helper = helper;
		
	}
	
	private void createReturnButtons(Composite container) {
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
				PyList returnVariables = (PyList)returnObj.__getattr__("value");
				int returnValueLength = returnVariables.__len__();
				String newReturnVariable = "${returnVariable"+String.valueOf(returnValueLength+1)+"}";
				new TableItem(returnTable, SWT.LEFT).setText(newReturnVariable);
				returnVariables.append(Py.newStringOrUnicode(newReturnVariable));
				previewArea.setText(helper.presentKeyword(keyword));
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
				if(selectedReturn!=null && returnTable.indexOf(selectedReturn)!=-1) {
					String returnVariableToRemove = selectedReturn.getText();
					PyList returnVariables = (PyList)returnObj.__getattr__("value");
					returnVariables.remove(Py.newStringOrUnicode(returnVariableToRemove));
					returnTable.remove(returnTable.indexOf(selectedReturn));
					previewArea.setText(helper.presentKeyword(keyword));					
				}
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
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
				PyList arguments = (PyList)argumentObj.__getattr__("value");
				int argumentLength = arguments.__len__();
				String newArgument = "${argument"+String.valueOf(argumentLength+1)+"}";
				new TableItem(argumentTable, SWT.LEFT).setText(new String[] {newArgument.substring(0,1), newArgument.substring(2, newArgument.length()-1)});
				arguments.append(Py.newStringOrUnicode(newArgument));
				previewArea.setText(helper.presentKeyword(keyword));
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
					PyList arguments = (PyList)argumentObj.__getattr__("value");
					arguments.remove(Py.newStringOrUnicode(argumentToRemove));
					argumentTable.remove(argumentTable.indexOf(selectedArgument));
					previewArea.setText(helper.presentKeyword(keyword));
				}
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
				// TODO Auto-generated method stub
				
			}
		});
    	
	}
	
	private void createArguments(Composite container) {
        Label argumentLabel = new Label(container, SWT.NONE);
        argumentLabel.setText("Argument");
        GridData argumentData = new GridData();
        argumentData.grabExcessHorizontalSpace = true;
        argumentData.horizontalAlignment = GridData.FILL;
        argumentTable = new Table(container, SWT.BORDER | SWT.FULL_SELECTION);
        argumentTable.setItemCount(2);
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
    	argumentObj = keyword.__getattr__("args");
    	for(Object arg:(PyList)argumentObj.__getattr__("value")) {
    		String argValue = (String)arg;
    		TableItem item = new TableItem(argumentTable, SWT.LEFT);
    		item.setText(new String[] {argValue.substring(0, 1), argValue.substring(2, argValue.length()-1)});
    	}
    	argumentTable.setLayoutData(argumentData);
    	argumentTable.addListener(SWT.MouseDown, e->{
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
					textEditor.addModifyListener(event->{
						String argType = selectedArgument.getText(0);
						String argName = selectedArgument.getText(1);
						String originArg = argType+"{"+argName+"}";
						PyList arguments = (PyList)argumentObj.__getattr__("value");
						int index = arguments.index(Py.newStringOrUnicode(originArg));
						String input = textEditor.getText();
						String newArg = argType+"{"+input+"}";
						selectedArgument.setText(column, input);
						arguments.set(index, newArg);
						this.updateReferences(keyword, originArg, input);
						previewArea.setText(helper.presentKeyword(keyword));
					});
					String curText = selectedArgument.getText(column);
					textEditor.setText(curText);
					tableEditor = textEditor;
				}
				else {
					Combo comboEditor = new Combo(argumentTable, SWT.READ_ONLY);
					comboEditor.setItems(variableLabels);
					comboEditor.addSelectionListener(new SelectionListener() {
						@Override
						public void widgetSelected(SelectionEvent e) {
							int selection = comboEditor.getSelectionIndex();
							String argType = selectedArgument.getText(0);
							String argName = selectedArgument.getText(1);
							String originArg = argType+"{"+argName+"}";
							PyList arguments = (PyList)argumentObj.__getattr__("value");
							int index = arguments.index(Py.newStringOrUnicode(originArg));
							selectedArgument.setText(column, argType);
							String selectionType = variableTypes[selection];
							selectedArgument.setText(0, selectionType);
							comboEditor.dispose();
							arguments.set(index, selectionType+"{"+argName+"}");
							previewArea.setText(helper.presentKeyword(keyword));
						}
						
						@Override
						public void widgetDefaultSelected(SelectionEvent e) {
							// TODO Auto-generated method stub
							
						}
					});
					
					String type = selectedArgument.getText(column);
					int typeIndex = Arrays.asList(variableTypes).indexOf(type);					
					String label = variableLabels[typeIndex];
					comboEditor.setText(label);
					tableEditor = comboEditor;
				}
				argumentEditor.setEditor(tableEditor, selectedArgument,column);
				tableEditor.forceFocus();
		});
    }

	private void createReturn(Composite container) {
        Label argument = new Label(container, SWT.NONE);
        argument.setText("Return");
        GridData returnData = new GridData();
        returnData.grabExcessHorizontalSpace = true;
        returnData.horizontalAlignment = GridData.FILL;
        returnTable = new Table(container, SWT.VIRTUAL | SWT.BORDER);
        returnTable.setItemCount(2);
        returnEditor = new TableEditor(returnTable);
        returnEditor.horizontalAlignment = SWT.LEFT;
        returnEditor.grabHorizontal = true;
        returnTable.setHeaderVisible(true);
        returnTable.setLinesVisible(true);
    	TableColumn returnColumn = new TableColumn(returnTable,SWT.LEFT);
    	returnColumn.setWidth(200);
    	returnColumn.setText("Return");
    	returnObj = keyword.__getattr__("return_");
    	for(Object ret:(PyList)returnObj.__getattr__("value")) {
    		String retValue = (String)ret;
    		TableItem item = new TableItem(returnTable, SWT.LEFT);
    		item.setText(retValue);
    	}
    	returnTable.setLayoutData(returnData);
    	returnTable.addSelectionListener(new SelectionListener() {
			
			@Override
			public void widgetSelected(SelectionEvent e) {
				selectedReturn = (TableItem)e.item;
				Control editor = returnEditor.getEditor();
				if(editor!=null)
					editor.dispose();
				Text textEditor= new Text(returnTable,SWT.None);
				textEditor.addModifyListener(event->{
					String originReturn = selectedReturn.getText();
					PyList returns = (PyList)returnObj.__getattr__("value");
					int index = returns.index(Py.newStringOrUnicode(originReturn));
					String input = textEditor.getText();
					selectedReturn.setText(input);
					returns.set(index, input);
					previewArea.setText(helper.presentKeyword(keyword));
				});
				String curText = selectedReturn.getText();
				textEditor.setText(curText);
	    		returnEditor.setEditor(textEditor, selectedReturn,0);
				textEditor.forceFocus();
				
			}
			
			@Override
			public void widgetDefaultSelected(SelectionEvent e) {
				// TODO Auto-generated method stub
				
			}
    	});
	}
    
    private void createPreviewArea(Composite container) {
    	previewLabel = new Label(container, SWT.VIRTUAL);
    	previewLabel.setText("Preview");
    	previewLabel.setVisible(false);
    	previewArea = new StyledText(container, SWT.BORDER);
    	GridData previewGrid = new GridData();
        previewGrid.grabExcessHorizontalSpace = true;
        previewGrid.horizontalAlignment = GridData.FILL;
        previewArea.setText(helper.presentKeyword(keyword));
        previewArea.setLayoutData(previewGrid);
        previewArea.setEditable(false);
        previewArea.setVisible(false);
    }

	@Override
	public void create() {
		super.create();
		setTitle("Change keyword signature");
        setMessage("Tips", IMessageProvider.INFORMATION);
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
		createReturn(container);
		createReturnButtons(container);
		createPreviewArea(container);
		return area;
	}
	
	@Override
	protected void createButtonsForButtonBar(Composite parent) {
		super.createButtonsForButtonBar(parent);
		Button preview = new Button(parent, SWT.PUSH);
		setButtonLayoutData(preview);
		preview.setText("Preview");
		preview.addMouseListener(new MouseListener() {
			
			@Override
			public void mouseUp(MouseEvent e) {
			
				
			}
			
			@Override
			public void mouseDown(MouseEvent e) {
				if(isPreview){
					isPreview = false;
					preview.setText("Preview");
					previewLabel.setVisible(false);
					previewArea.setVisible(false);
				}
				else {
					isPreview = true;
					preview.setText("<< Preview");
					String previewText = helper.presentKeyword(keyword);
					previewArea.setText(previewText);
					previewLabel.setVisible(true);
					previewArea.setVisible(true);
				}
				
			}
			
			@Override
			public void mouseDoubleClick(MouseEvent e) {
			
				
			}
		});
	}
	
	@Override
	protected void okPressed() {
		super.okPressed();
		
	}
	
	private void updateReferences(PyObject keyword, String oldName, String newName) {
		PyList references = helper.getLocalVariableReferences(keyword, oldName);
		helper.renameReferencesImpl(references, oldName, newName);
		
	}

}
