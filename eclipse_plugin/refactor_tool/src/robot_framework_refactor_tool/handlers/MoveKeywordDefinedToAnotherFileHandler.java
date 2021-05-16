package robot_framework_refactor_tool.handlers;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.window.Window;
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
			pluginHelper.showMessage("Robot_framework_refactor_tool", RenameKeywordHandler.TIP_MESSAGE);
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
			this.pluginHelper.showMessage("Robot_framework_refactor_tool", "Defined keyword:"+movedkwName+"\nNot found");
			return null;
		}
		pluginHelper.showMessage("Robot_framework_refactor_tool", "\"Move keyword defined to another file\" will start.\n\nThe following steps are the entire process.\n\nStep1: Choose the file you want to move the keyword into.\n\nStep2: Import new resource automatically for files that not import the new resource.");
		Node root = new NodeBuilder().buildForModels(projectModels);
		FileSelectionView fileView= pluginHelper.fileSelectionView();
		fileView.update(root, this);
		pluginHelper.showMessage("Step1: Choose the file you want to move the keyword into", "Please choose the file you want to move the keyword into.");

		return event;
	}

	public void afterChoosingFileToInsertMovedKeyword(String targetPath) {
		PyObject targetModel = this.newRefactorHelper.buildFileModel(targetPath);
		this.newRefactorHelper.removeDefinedKeyword(this.fromModel, this.movedKeyword);
		this.newRefactorHelper.insertDefinedKeyword(targetModel, this.movedKeyword);
		PyList modelsUsingMovedKeyword = this.newRefactorHelper.getModelsUsingKeyword(this.editorLocation, this.movedkwName);
		PyList modelsWithoutImporting = this.newRefactorHelper.getModelsWithoutImportTargetResource(this.movedkwName, this.editorLocation, targetPath);
		if(modelsWithoutImporting.size() > 0) {
			this.pluginHelper.showMessage("Step2: Import new resource automatically for files that not import the new resource", "Number of files that not import the new resource is " + modelsWithoutImporting.size() + ".\n\nThe system has imported for it(them).");
		}
		for (int index = 0;index < modelsWithoutImporting.size(); index++) {
			PyObject modelWithoutImporting = (PyObject)modelsWithoutImporting.get(index);
			String pathNotImport = modelWithoutImporting.__getattr__("source").toString();
			pathNotImport = pathNotImport.substring(0, pathNotImport.lastIndexOf("/"));
			Path pathAbsolute = Paths.get(targetPath);
	        Path pathBase = Paths.get(pathNotImport);
	        Path pathRelative = pathBase.relativize(pathAbsolute);
			String newResourceValue = pathRelative.toString().replace("\\", "/");
			this.newRefactorHelper.importNewResourceForModelWithoutImporting(modelWithoutImporting, newResourceValue);
		}
		List<String> pathOfFilesCanRun = new ArrayList<>();
		for(Object model : modelsUsingMovedKeyword) {
			if(((PyObject)model).__getattr__("source").toString().indexOf(".robot") != -1) {
				pathOfFilesCanRun.add(((PyObject)model).__getattr__("source").toString());
			}
		}
		InputDialog finishMovingDialog = new InputDialog(window.getShell(), "Finish moving the keyword into target file", "Success move the keyword to the target file.\n\nNumber of relative test cases is " + pathOfFilesCanRun.size() + ".\n\nDo you want to run the test cases?\n\nYou can get the path to check the moved keyword.", targetPath, null);
		if(finishMovingDialog.open() == Window.OK) {
			this.pluginHelper.runTestCasesAndOpenReport(pathOfFilesCanRun);			
		}
	}
}
