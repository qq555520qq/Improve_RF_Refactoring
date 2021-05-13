package robot_framework_refactor_tool.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.resources.IResource;
import org.eclipse.core.runtime.CoreException;
import org.eclipse.jface.window.Window;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.handlers.HandlerUtil;
import org.python.core.Py;
import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyObject;

import helper.PluginHelper;
import helper.RefactorHelper;
import robot_framework_refactor_tool.views.ChangeSignatureDialog;
import robot_framework_refactor_tool.views.ModifyAction;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.RenameAction;
import robot_framework_refactor_tool.views.ShowReferencesView;

public class ChangeSignatureHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private RefactorHelper refactorHelper;
	public ChangeSignatureHandler() {
		refactorHelper = PluginHelper.getRefactorHelper();
	}
	
	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(refactorHelper==null) {
			pluginHelper.showMessage("Robot_framework_refactor_tool", RenameKeywordHandler.TIP_MESSAGE);
			return null;
		}	
		String kwName = pluginHelper.getUserSelectionText();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		PyObject projectRoot = this.refactorHelper.buildTestData(projectPath);
		PyObject keyword = this.refactorHelper.getKeyword(projectRoot, kwName, editorLocation);
		ChangeSignatureDialog dialog = new ChangeSignatureDialog(window.getShell(), refactorHelper, keyword);
		if(dialog.open()==Window.OK) {
			PyObject testDataOfKeyword = keyword.__getattr__("parent").__getattr__("parent");
			refactorHelper.save(testDataOfKeyword);
			PyList references = (PyList)this.refactorHelper.getKeywordReferences(projectRoot, keyword);
			Node root = new NodeBuilder().build(references);
			ShowReferencesView view= pluginHelper.showReferencesView();
			RenameAction saveAction = createSaveAction(window, view, references);
			ModifyAction modifyAction = createModifyAction();
			view.update(root, saveAction,modifyAction);
		}
		
		return event;
	}
	
	public ModifyAction createModifyAction() {
		ModifyAction action = (step, userInput) -> refactorHelper.modifyReference((PyObject)step.getData(), userInput);
		return action;
	}
	
	public RenameAction createSaveAction(IWorkbenchWindow window, ShowReferencesView view, PyList kwReferences) {
		RenameAction action = (reference) -> {	
			for(Object object:kwReferences) {
				PyDictionary referenceDict = (PyDictionary)object;
				PyObject testDataFile = referenceDict.get(Py.newString("testdata"));
				refactorHelper.save(testDataFile);
			}
			pluginHelper.showMessage("Robot_framework_refactor_tool", "Sucess modify signature");
			view.update(null, null, null);
			try {
				pluginHelper.getCurrentEditorFile().getFile().refreshLocal(IResource.DEPTH_ONE, null);
			} catch (CoreException e) {
				e.printStackTrace();
			}
		};
		return action;
	}

}
