package robot_framework_refactor_tool.handlers;


import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.window.Window;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.python.core.PyList;
import org.python.core.PyObject;

import helper.PluginHelper;
import helper.NewRefactorHelper;
import robot_framework_refactor_tool.views.CreateANewKeyword;
import robot_framework_refactor_tool.views.AddArgumentsForKeywordReplacingSameSteps;
import robot_framework_refactor_tool.views.FileSelectionView;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.SameKeywordsSelectionView;
import robot_framework_refactor_tool.views.SameStepsBlock;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class WrapStepsAsANewKeywordHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private NewRefactorHelper newRefactorHelper;
	private PyList modelsBeforeWraping;
	private PyList modelsWithSameKeywords = new PyList();
	private PyList newKeywordBody;
	private String newKwName;
	private String newKwPath;
	private IWorkbenchWindow window;
	private PyList newArgumentsOfNewKeyword;
	private String editorLocation;
	public WrapStepsAsANewKeywordHandler() {
		this.newRefactorHelper = PluginHelper.getNewRefactorHelper();
	}
	
	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(this.newRefactorHelper==null) {
			pluginHelper.showMessage("Robot_framework_refactor_tool", RenameKeywordHandler.TIP_MESSAGE);
			return null;
		}
		String projectPath = pluginHelper.getCurrentProjectLocation();
		editorLocation = pluginHelper.getCurrentEditorLocation();
		PyList projectModels = this.newRefactorHelper.buildProjectModels(projectPath);
		modelsBeforeWraping = new PyList(projectModels.getArray());
		PyObject fileModel = this.newRefactorHelper.buildFileModel(editorLocation);
		int startLine = this.pluginHelper.getUserSelectionStartLine() + 1;
		int endLine = this.pluginHelper.getUserSelectionEndLine() + 1;
		PyList steps = this.newRefactorHelper.getStepsThatWillBeWraped(fileModel, startLine, endLine);
		if(steps.size() == 0) {
			this.pluginHelper.showMessage("Robot_framework_refactor_tool", "Steps you choose are not found.");
			return null;
		}
		this.newArgumentsOfNewKeyword = this.newRefactorHelper.getVariablesNotDefinedInSteps(steps);
		this.modelsWithSameKeywords = this.newRefactorHelper.getSameKeywordsWithSteps(projectModels, steps);
		pluginHelper.showMessage("Robot_framework_refactor_tool", "\"Wrap steps as a new keyword\" will start.\n\nThe following steps are the entire process.\n\nStep1: Create a new keyword.\n\nStep2: Replace the same steps with new keyword.\n\nStep3: Import new resource automatically for files that not import the new resource.");
		CreateANewKeyword createANewKeywordDialog = new CreateANewKeyword(window.getShell(), this.newArgumentsOfNewKeyword);
		if(createANewKeywordDialog.open()==Window.OK) {
			PyList argumentsTokens = new PyList();
			if(this.newArgumentsOfNewKeyword.size() != 0) {
				argumentsTokens = this.newRefactorHelper.buildTokensOfArgumentsInNewKeyword(this.newArgumentsOfNewKeyword);
			}
			this.newKeywordBody = this.newRefactorHelper.getNewKeywordBodyWithStepsAndNewArguments(steps, argumentsTokens);
			newKwName = createANewKeywordDialog.getNewKeywordName();
			Node root = new NodeBuilder().buildForModels(projectModels);
			FileSelectionView fileView= pluginHelper.fileSelectionView();
			fileView.update(root, this);
			pluginHelper.showMessage("Step1: Create a new keyword", "Please choose the file to create the new keyword.");
		}

		return event;
	}

	public void afterChoosingFileToCreateKeyword(String targetPath) {
		newKwPath = targetPath;
		this.newRefactorHelper.createNewKeywordForFile(targetPath, this.newKwName, this.newKeywordBody);
		if (this.modelsWithSameKeywords.size() > 0) {			
			Node sameKeywordsRoot = new NodeBuilder().buildForSameKeywords(this.modelsWithSameKeywords);
			SameKeywordsSelectionView sameKeywordsView = pluginHelper.sameKeywordsSelectionView();
			sameKeywordsView.update(sameKeywordsRoot, this, this.window, this.newRefactorHelper);
			pluginHelper.showMessage("Step2: Replace the same steps with new keyword.", "Please choose the file(s) with same steps to replace it(them) with new keyword.\n\nClicking node with 'Ctrl' can select multiple and unselect.\n\nDouble clicking can present same steps.");
		}else {
			this.afterChoosingReplacedSteps(new PyList());
		}
	}

	public Object afterChoosingReplacedSteps(PyList sameKeywordsBlocks) {
		PyList modelsWithReplacing = new PyList();
		for (int index = 0;index < sameKeywordsBlocks.size();index++) {
			PyList newKeywordArgs = new PyList();
			PyList sameStepsBlock = (PyList)((SameStepsBlock)sameKeywordsBlocks.get(index)).getData();
			AddArgumentsForKeywordReplacingSameSteps newkeywordArgsDialog = new AddArgumentsForKeywordReplacingSameSteps(window.getShell(), this.newRefactorHelper, sameStepsBlock, newKeywordArgs, this.newArgumentsOfNewKeyword);
			if(newkeywordArgsDialog.open()==Window.OK) {
				PyObject modelWithReplacing = this.newRefactorHelper.replaceStepsWithKeywordAndGetModelsWithReplacing(newKwName, newKeywordArgs, sameStepsBlock);
				modelsWithReplacing.add(modelWithReplacing);
			}
			else {
				this.newRefactorHelper.saveModels(modelsBeforeWraping);
				this.pluginHelper.showMessage("Stop wrapping steps as a new keyword", "Revert every change.");
				return null;
			}
		}
		if(modelsWithReplacing.size() > 0) {
			PyList modelsWithoutImporting = this.newRefactorHelper.getModelsWithoutImportingNewResourceFromModelsWithReplacement(newKwName, modelsWithReplacing, this.newKwPath);
			if(modelsWithoutImporting.size() > 0) {
				this.pluginHelper.showMessage("Step3: Import new resource automatically for files that not import the new resource", "Number of files that not import the new resource is " + modelsWithoutImporting.size() + ".\n\nThe system has imported for it(them).");
			}
			for (int index = 0;index < modelsWithoutImporting.size(); index++) {
				PyObject modelWithoutImporting = (PyObject)modelsWithoutImporting.get(index);
				String pathNotImport = modelWithoutImporting.__getattr__("source").toString();
				pathNotImport = pathNotImport.substring(0, pathNotImport.lastIndexOf("/"));
				Path pathAbsolute = Paths.get(this.newKwPath);
		        Path pathBase = Paths.get(pathNotImport);
		        Path pathRelative = pathBase.relativize(pathAbsolute);
				String newResourceValue = pathRelative.toString().replace("\\", "/");
				this.newRefactorHelper.importNewResourceForModelWithoutImporting(modelWithoutImporting, newResourceValue);
			}
		}
		InputDialog getNewKeywordPathDialog = new InputDialog(window.getShell(), "Finish wrapping steps as a new keyword", "Success wrap steps as a new keyword.\n\nYou can get the path to check the new keyword.\n\n Do you want to run the test case that you refactor?", newKwPath, null);
		if(getNewKeywordPathDialog.open() == Window.OK & editorLocation.indexOf(".robot") != -1) {
			List<String> paths = new ArrayList<>();
			paths.add(editorLocation);
			this.pluginHelper.runTestCasesAndOpenReport(paths);
		}
		return null;
	}
}
