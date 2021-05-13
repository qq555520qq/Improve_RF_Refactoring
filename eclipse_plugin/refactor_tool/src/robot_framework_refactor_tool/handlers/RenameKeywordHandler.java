package robot_framework_refactor_tool.handlers;

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
import org.python.core.PyList;
import org.python.core.PyObject;
import helper.PluginHelper;
import helper.RefactorHelper;
import robot_framework_refactor_tool.views.ShowReferencesView;
import robot_framework_refactor_tool.views.Step;
import robot_framework_refactor_tool.views.ModifyAction;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.RenameAction;;

public class RenameKeywordHandler extends AbstractHandler {
	public static String TIP_MESSAGE = "Please Configure the python site-package path and make sure you have installed rf-refactoring !!!\nType 'pip install JoeLiu-RF-Refactoring -U' in your terminal\nAfter fix it please restart the eclipse.";
	private RefactorHelper refactorHelper;
	private PluginHelper pluginHelper;
	public RenameKeywordHandler() {
		refactorHelper = PluginHelper.getRefactorHelper();
	}
	
	public RenameAction createRenameAction(IWorkbenchWindow window, ShowReferencesView view, PyObject keyword, String newName) {
		String variableName = keyword.__getattr__("name").toString();
		RenameAction action = (reference) -> {
			this.refactorHelper.renameKeywordDef(keyword, newName);
			this.refactorHelper.renameReferences(reference, variableName, newName);
			view.update(null, null, null);
			pluginHelper.showMessage("Robot_framework_refactor_tool", "Sucess rename keyowrd '"+variableName+"' to '"+newName+"'.");
			try {
				pluginHelper.getCurrentEditorFile().getFile().refreshLocal(IResource.DEPTH_ONE, null);
			} catch (CoreException e) {
				e.printStackTrace();
			}
		};
		return action;
	}

	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(refactorHelper==null) {
			pluginHelper.showMessage("Robot_framework_refactor_tool", TIP_MESSAGE);
			return null;
		}
		String oldKwName = pluginHelper.getUserSelectionText();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		PyObject projectRoot = this.refactorHelper.buildTestData(projectPath);
		PyObject keyword = this.refactorHelper.getKeyword(projectRoot, oldKwName, editorLocation);
		if(keyword == Py.None) 
			pluginHelper.showMessage("Robot_framework_refactor_tool", "Keyword name:"+oldKwName+"\nNot found");		
		else {
			InputDialog newNameDialog = new InputDialog(window.getShell(), "Rename Keyword", "Input the new Keyword Name", "", new IInputValidator() {		
				@Override
				public String isValid(String newText) {
					if(newText.isEmpty())
						return "Keyword Name Should not be empty!!!";
					return null;
				}
			});
			if(newNameDialog.open() == Window.CANCEL)
				return null;
			String newKwName = newNameDialog.getValue();
			PyList references = (PyList)this.refactorHelper.getKeywordReferences(projectRoot, keyword);
			Node root = new NodeBuilder().build(references);
			ShowReferencesView view= pluginHelper.showReferencesView();
			RenameAction renameKeyword = createRenameAction(window, view, keyword, newKwName);
			view.update(root, renameKeyword,null);
		}
		return null;
	}
	
	


}
