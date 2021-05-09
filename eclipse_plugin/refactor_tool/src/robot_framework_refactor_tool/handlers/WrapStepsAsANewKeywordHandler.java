package robot_framework_refactor_tool.handlers;

import java.util.List;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.resources.IResource;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.jface.dialogs.IInputValidator;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.window.Window;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.python.core.Py;
import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyObject;

import helper.PluginHelper;
import helper.NewRefactorHelper;
import robot_framework_refactor_tool.views.AddArgumentsForNewKeyword;
import robot_framework_refactor_tool.views.FileSelectionView;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.SameKeywordsSelectionView;
import robot_framework_refactor_tool.views.SameStepsBlock;

public class WrapStepsAsANewKeywordHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private NewRefactorHelper newRefactorHelper;
	private PyList modelsWithSameKeywords;
	private PyList newKeywordBody;
	private String newKwName;
	private String newKwPath;
	private IWorkbenchWindow window;
	public WrapStepsAsANewKeywordHandler() {
		newRefactorHelper = PluginHelper.getNewRefactorHelper();
	}
	
	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(newRefactorHelper==null) {
			pluginHelper.showMessage("No helper");
			return null;
		}
//		String kwName = pluginHelper.getUserSelectionText();
		PyList newArguments = new PyList();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		PyList projectModels = this.newRefactorHelper.buildProjectModels(projectPath);
		PyObject fileModel = this.newRefactorHelper.buildFileModel(editorLocation);
		int startLine = this.pluginHelper.getUserSelectionStartLine() + 1;
		int endLine = this.pluginHelper.getUserSelectionEndLine() + 1;
		PyList steps = this.newRefactorHelper.getStepsThatWillBeWraped(fileModel, startLine, endLine);
		this.modelsWithSameKeywords = this.newRefactorHelper.getSameKeywordsWithSteps(projectModels, steps);
		AddArgumentsForNewKeyword addArgDialog = new AddArgumentsForNewKeyword(window.getShell(), newArguments, "Add arguments for new keyword");
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
		Node sameKeywordsRoot = new NodeBuilder().buildForSameKeywords(this.modelsWithSameKeywords);
		SameKeywordsSelectionView sameKeywordsView = pluginHelper.sameKeywordsSelectionView();
		sameKeywordsView.update(sameKeywordsRoot, this);
		pluginHelper.showMessage("Please choose the file(s) with same steps to replace it(them) with new keyword.");
	}

	public void afterChoosingReplacedSteps(PyList sameKeywordsBlocks) {
		PyList modelsWithReplacing = new PyList();
		for (int index = 0;index < sameKeywordsBlocks.size();index++) {
			PyList newKeywordArgs = new PyList();
			AddArgumentsForNewKeyword newkeywordArgsDialog = new AddArgumentsForNewKeyword(window.getShell(), newKeywordArgs, "Add arguments for keyword that will be used to replace steps");
			PyList sameStepsBlock = (PyList)((SameStepsBlock)sameKeywordsBlocks.get(index)).getData();
			if(newkeywordArgsDialog.open()==Window.OK) {
				PyObject modelWithReplacing = this.newRefactorHelper.replaceStepsWithKeywordAndGetModelsWithReplacing(newKwName, newKeywordArgs, sameStepsBlock);
				modelsWithReplacing.add(modelWithReplacing);
			}
		}
		PyList modelsWithoutImporting = this.newRefactorHelper.getModelsWithoutImportingNewResourceFromModelsWithReplacement(newKwName, modelsWithReplacing, newKwPath);
		
	}
}
