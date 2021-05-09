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
import helper.NewRefactorHelper;
import robot_framework_refactor_tool.views.ChangeSignatureDialog;
import robot_framework_refactor_tool.views.ModifyAction;
import robot_framework_refactor_tool.views.Node;
import robot_framework_refactor_tool.views.NodeBuilder;
import robot_framework_refactor_tool.views.RenameAction;
import robot_framework_refactor_tool.views.ShowReferencesView;

public class MoveKeywordDefinedToAnotherFileHandler extends AbstractHandler {
	
	private PluginHelper pluginHelper;
	private NewRefactorHelper newRefactorHelper;
	public MoveKeywordDefinedToAnotherFileHandler() {
		newRefactorHelper = PluginHelper.getNewRefactorHelper();
	}

	@Override
	public Object execute(ExecutionEvent event) throws ExecutionException {
		IWorkbenchWindow window = HandlerUtil.getActiveWorkbenchWindowChecked(event);
		this.pluginHelper = new PluginHelper(window);
		if(newRefactorHelper==null) {
			pluginHelper.showMessage(RenameKeywordHandler.TIP_MESSAGE);
			return null;
		}
//		String kwName = pluginHelper.getUserSelectionText();
		String editorLocation = pluginHelper.getCurrentEditorLocation();
		String projectPath = pluginHelper.getCurrentProjectLocation();
		PyObject projectRoot = this.newRefactorHelper.buildProjectModels(projectPath);
		System.out.print("This is test");

		return event;
	}

}
