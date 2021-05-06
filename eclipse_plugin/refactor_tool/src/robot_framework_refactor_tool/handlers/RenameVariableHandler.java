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
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.RenameAction;
import robot_framework_refactor_tool.views.ShowReferencesView;
public class RenameVariableHandler extends AbstractHandler {
	private RefactorHelper refactorHelper;
	private PluginHelper pluginHelper;
	
	public RenameAction createRenameAction(IWorkbenchWindow window, ShowReferencesView view, PyObject variable, String newVariableName) {
		String variableName = variable.__getattr__("name").toString();
		RenameAction action = (reference) -> {
			this.refactorHelper.renameVariableDef(variable, newVariableName);
			this.refactorHelper.renameReferences(reference, variableName, newVariableName);
			view.update(null, null, null);
			pluginHelper.showMessage("Sucess rename variable '"+variableName+"' to '"+newVariableName+"'.");
			try {
				pluginHelper.getCurrentEditorFile().getFile().refreshLocal(IResource.DEPTH_ONE, null);
			} catch (CoreException e) {
				e.printStackTrace();
			}
		};
		return action;
	}
	
	public RenameVariableHandler() {
		refactorHelper = PluginHelper.getRefactorHelper();
	}

	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException{
		IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(refactorHelper==null) {
			pluginHelper.showMessage(RenameKeywordHandler.TIP_MESSAGE);
			return null;
		}
		String variableName = pluginHelper.getUserSelectionText();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		PyObject projectRoot = this.refactorHelper.buildTestData(projectPath);
		PyObject variable = this.refactorHelper.getVariable(projectRoot, variableName, editorLocation);
		if(variable == Py.None) 
			pluginHelper.showMessage("Variable :"+variableName+"\nNot found");
		else {
			InputDialog newNameDialog = new InputDialog(window.getShell(), "Rename Variable", "Input the new Variable Name", "", new IInputValidator() {
				@Override
				public String isValid(String newText) {
						if(newText.isEmpty())
							return "Variable Name Should not be empty!!!";
						return null;
					}
				});
			if(newNameDialog.open() == Window.CANCEL)
				return null;
			String newVariableName = newNameDialog.getValue();
			PyList references = (PyList)this.refactorHelper.getVariableReferences(projectRoot, variable);
			Node root = new NodeBuilder().build(references);
			ShowReferencesView view = pluginHelper.showReferencesView();
			RenameAction renameVariable = createRenameAction(window, view, variable, newVariableName);
			view.update(root, renameVariable, null);
		}
	return null;
}

}
