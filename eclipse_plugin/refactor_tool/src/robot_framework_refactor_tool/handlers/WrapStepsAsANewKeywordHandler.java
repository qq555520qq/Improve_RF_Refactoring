package robot_framework_refactor_tool.handlers;

import java.util.List;

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
import org.python.core.PyList;
import org.python.core.PyObject;

import helper.PluginHelper;
import helper.NewRefactorHelper;
import robot_framework_refactor_tool.views.AddArgumentsForNewKeyword;
import robot_framework_refactor_tool.views.AddArgumentsForKeywordReplacingSameSteps;
import robot_framework_refactor_tool.views.FileSelectionView;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.SameKeywordsSelectionView;
import robot_framework_refactor_tool.views.SameStepsBlock;

public class WrapStepsAsANewKeywordHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private NewRefactorHelper newRefactorHelper;
	private PyList modelsWithSameKeywords = new PyList();
	private PyList newKeywordBody;
	private String newKwName;
	private String newKwPath;
	private IWorkbenchWindow window;
	public WrapStepsAsANewKeywordHandler() {
		this.newRefactorHelper = PluginHelper.getNewRefactorHelper();
	}
	
	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(this.newRefactorHelper==null) {
			pluginHelper.showMessage("No helper");
			return null;
		}
		PyList newArguments = new PyList();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		PyList projectModels = this.newRefactorHelper.buildProjectModels(projectPath);
		PyObject fileModel = this.newRefactorHelper.buildFileModel(editorLocation);
		int startLine = this.pluginHelper.getUserSelectionStartLine() + 1;
		int endLine = this.pluginHelper.getUserSelectionEndLine() + 1;
		PyList steps = this.newRefactorHelper.getStepsThatWillBeWraped(fileModel, startLine, endLine);
		if(steps.size() == 0) {
			this.pluginHelper.showMessage("Steps you choose are not found.");
			return null;
		}
		this.modelsWithSameKeywords = this.newRefactorHelper.getSameKeywordsWithSteps(projectModels, steps);
		AddArgumentsForNewKeyword addArgDialog = new AddArgumentsForNewKeyword(window.getShell(), newArguments);
		if(addArgDialog.open()==Window.OK) {
			PyList argumentsTokens = new PyList();
			if(newArguments.size() != 0) {
				argumentsTokens = this.newRefactorHelper.buildTokensOfArgumentsInNewKeyword(newArguments);
			}
			this.newKeywordBody = this.newRefactorHelper.getNewKeywordBodyWithStepsAndNewArguments(steps, argumentsTokens);
			InputDialog newNameDialog = new InputDialog(window.getShell(), "New Keyword Name", "Input the new Keyword Name", "", new IInputValidator() {
				@Override
				public String isValid(String newText) {
					if(newText.isEmpty())
						return "Keyword Name Should not be empty!!!";
					return null;
				}
			});
			if(newNameDialog.open() == Window.CANCEL)
				return null;
			newKwName = newNameDialog.getValue();
			Node root = new NodeBuilder().buildForModels(projectModels);
			FileSelectionView fileView= pluginHelper.fileSelectionView();
			fileView.update(root, this);
			pluginHelper.showMessage("Please choose the file to insert new keyword.");
		}

		return event;
	}

	public void afterChoosingFileToInsertKeyword(String targetPath) {
		newKwPath = targetPath;
		this.newRefactorHelper.createNewKeywordForFile(targetPath, this.newKwName, this.newKeywordBody);
		if (this.modelsWithSameKeywords.size() > 0) {			
			Node sameKeywordsRoot = new NodeBuilder().buildForSameKeywords(this.modelsWithSameKeywords);
			SameKeywordsSelectionView sameKeywordsView = pluginHelper.sameKeywordsSelectionView();
			sameKeywordsView.update(sameKeywordsRoot, this, this.window, this.newRefactorHelper);
			pluginHelper.showMessage("Please choose the file(s) with same steps to replace it(them) with new keyword.\n\nClicking node with 'Ctrl' can select multiple and unselect.\n\nDouble clicking can present same steps.");
		}else {
			this.afterChoosingReplacedSteps(new PyList());
		}
	}

	public void afterChoosingReplacedSteps(PyList sameKeywordsBlocks) {
		PyList modelsWithReplacing = new PyList();
		for (int index = 0;index < sameKeywordsBlocks.size();index++) {
			PyList newKeywordArgs = new PyList();
			PyList sameStepsBlock = (PyList)((SameStepsBlock)sameKeywordsBlocks.get(index)).getData();
			AddArgumentsForKeywordReplacingSameSteps newkeywordArgsDialog = new AddArgumentsForKeywordReplacingSameSteps(window.getShell(), this.newRefactorHelper, sameStepsBlock, newKeywordArgs);
			if(newkeywordArgsDialog.open()==Window.OK) {
				PyObject modelWithReplacing = this.newRefactorHelper.replaceStepsWithKeywordAndGetModelsWithReplacing(newKwName, newKeywordArgs, sameStepsBlock);
				modelsWithReplacing.add(modelWithReplacing);
			}
		}
		if(modelsWithReplacing.size() > 0) {
			PyList modelsWithoutImporting = this.newRefactorHelper.getModelsWithoutImportingNewResourceFromModelsWithReplacement(newKwName, modelsWithReplacing, this.newKwPath);
			if(modelsWithoutImporting.size() > 0) {		
				this.pluginHelper.showMessage("Number of models without importing the new resource is " + modelsWithoutImporting.size() + ".\n\nPlease import resource for it(them).");
			}
			for (int index = 0;index < modelsWithoutImporting.size(); index++) {
				PyObject modelWithoutImporting = (PyObject)modelsWithoutImporting.get(index);
				String dialogMessage = "Please input new resource value for model without importing resource where new keyword is\n\nPath of new keyword:\n" + this.newKwPath + "\n\nPath of model without importing:\n" + modelWithoutImporting.__getattr__("source");
				String FileNameWhereNewKeywordIs = newKwPath.substring(newKwPath.lastIndexOf("/")+1);
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
		}
		this.pluginHelper.showMessage("Success wrap steps as a new keyword.\n\nPlease go to the file checking new keyword again.");
		InputDialog getNewKeywordPathDialog = new InputDialog(window.getShell(), "Path of new keyword", "You can get the path to check the new keyword", newKwPath, null){
			  @Override
			  public void create() {
				super.create();
		        Button cancelButton= getButton(IDialogConstants.CANCEL_ID);
		    	cancelButton.setVisible(false);
			  }
		};
		getNewKeywordPathDialog.open();
	}
}
