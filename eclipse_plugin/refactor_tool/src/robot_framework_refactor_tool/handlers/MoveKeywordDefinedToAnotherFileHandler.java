package robot_framework_refactor_tool.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.IDialogConstants;
import org.eclipse.jface.dialogs.IInputValidator;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.window.Window;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Control;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.python.core.Py;
import org.python.core.PyList;
import org.python.core.PyObject;

import helper.PluginHelper;
import helper.NewRefactorHelper;
import robot_framework_refactor_tool.views.FileSelectionView;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;

public class MoveKeywordDefinedToAnotherFileHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private NewRefactorHelper newRefactorHelper;
	private PyObject movedKeyword;
	private String movedkwName;
	private String editorLocation;
	private PyObject fromModel;
	private IWorkbenchWindow window;
	public MoveKeywordDefinedToAnotherFileHandler() {
		newRefactorHelper = PluginHelper.getNewRefactorHelper();
	}

	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		this.window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(newRefactorHelper==null) {
			pluginHelper.showMessage(RenameKeywordHandler.TIP_MESSAGE);
			return null;
		}
		String projectPath = this.pluginHelper.getCurrentProjectLocation();
		PyList projectModels = this.newRefactorHelper.buildProjectModels(projectPath);
		this.editorLocation = this.pluginHelper.getCurrentEditorLocation();
		this.fromModel = this.newRefactorHelper.buildFileModel(editorLocation);
		this.movedkwName = this.pluginHelper.getUserSelectionText();
		int keywordLine = this.pluginHelper.getUserSelectionStartLine() + 1;
		this.movedKeyword = this.newRefactorHelper.getMovedKeywordNodeFromModel(fromModel, movedkwName, keywordLine);
		if(this.movedKeyword == Py.None) {
			this.pluginHelper.showMessage("Defined keyword:"+movedkwName+"\nNot found");
			return null;
		}
		Node root = new NodeBuilder().buildForModels(projectModels);
		FileSelectionView fileView= pluginHelper.fileSelectionView();
		fileView.update(root, this);
		pluginHelper.showMessage("Please choose the file to insert moved keyword.");
		
		

		return event;
	}

	public void afterChoosingFileToInsertMovedKeyword(String targetPath) {
		PyObject targetModel = this.newRefactorHelper.buildFileModel(targetPath);
		this.newRefactorHelper.removeDefinedKeyword(this.fromModel, this.movedKeyword);
		this.newRefactorHelper.insertDefinedKeyword(targetModel, this.movedKeyword);
		PyList modelsWithoutImporting = this.newRefactorHelper.getModelsWithoutImportTargetResource(this.movedkwName, this.editorLocation, targetPath);
		if(modelsWithoutImporting.size() > 0) {			
			this.pluginHelper.showMessage("Number of models without importing the new resource is " + modelsWithoutImporting.size() + ".\n\nPlease import resource for it(them).");
		}
		for (int index = 0;index < modelsWithoutImporting.size(); index++) {
			PyObject modelWithoutImporting = (PyObject)modelsWithoutImporting.get(index);
			String dialogMessage = "Please input new resource value for model without importing resource where moved keyword is\n\nPath of moved keyword:\n" + targetPath + "\n\nPath of model without importing:\n" + modelWithoutImporting.__getattr__("source");
			String FileNameWhereNewKeywordIs = targetPath.substring(targetPath.lastIndexOf("/")+1);
			InputDialog newResourceDialog = new InputDialog(window.getShell(), "New resource value", dialogMessage, FileNameWhereNewKeywordIs, new IInputValidator() {
				@Override
				public String isValid(String newText) {
					if(newText.isEmpty())
						return "Resource value Should not be empty!!!";
					return null;
				}
			}){
				  @Override
				  public void create() {
					super.create();
			        Button cancelButton= getButton(IDialogConstants.CANCEL_ID);
			    	cancelButton.setVisible(false);
				  }
		          @Override
		          protected Control createDialogArea(Composite parent) {
		            Control res = super.createDialogArea(parent);
		            ((GridData) this.getText().getLayoutData()).widthHint = 1000;
		            return res;
		          }
		        };
			if(newResourceDialog.open()==Window.OK) {
				String newResourceValue = newResourceDialog.getValue();
				this.newRefactorHelper.importNewResourceForModelWithoutImporting(modelWithoutImporting, newResourceValue);
			}
		}
		this.pluginHelper.showMessage("Success move the keyword to the target file.\n\nPlease go to the file checking the moved keyword again.");
		InputDialog getMovedKeywordPathDialog = new InputDialog(window.getShell(), "Path of moved keyword", "You can get the path to check the moved keyword", targetPath, null){
			  @Override
			  public void create() {
				super.create();
		        Button cancelButton= getButton(IDialogConstants.CANCEL_ID);
		    	cancelButton.setVisible(false);
			  }
		};
		getMovedKeywordPathDialog.open();
	}
}
