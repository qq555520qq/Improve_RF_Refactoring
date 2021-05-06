package helper;

import java.util.Properties;

import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.resources.IProject;
import org.eclipse.core.runtime.preferences.InstanceScope;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.preference.IPreferenceStore;
import org.eclipse.jface.text.TextSelection;
import org.eclipse.jface.viewers.ISelection;
import org.eclipse.ui.IFileEditorInput;
import org.eclipse.ui.IWorkbenchWindow;
import org.eclipse.ui.preferences.ScopedPreferenceStore;
import org.python.util.PythonInterpreter;

import robot_framework_refactor_tool.views.ShowReferencesView;

public class PluginHelper {
	private IWorkbenchWindow window;
	public PluginHelper(IWorkbenchWindow window) {
		this.window = window;
	}
	
	public static String getPythonHome() {
		IPreferenceStore preferenceStore = new ScopedPreferenceStore(InstanceScope.INSTANCE, "robot_framework_refactor_tool.preference");
		return preferenceStore.getString("PYTHON");
	}
	
	public static RefactorHelper getRefactorHelper() {
		RefactorHelper refactorHelper=null;
		String pythonHome = RefactorHelper.processPath(PluginHelper.getPythonHome());
		try {
			String jythonPath = RefactorHelper.processPath(pythonHome+"/rfrefactoring/jython-standalone-2.7.2b3.jar");
			PluginHelper.initPython(jythonPath, pythonHome);
			refactorHelper = new RefactorHelper(new String[] {});
		}catch(Exception e) {
			
		}
		return refactorHelper;
	}
	
	public static void initPython(String pythonHome, String sitePath) {
		Properties props = new Properties();
		props.put("python.home", pythonHome);
		props.put("python.path", sitePath);
		Properties preprops = System.getProperties();
		PythonInterpreter.initialize(preprops, props, new String[]{});
	}
	
	public String getUserSelectionText() throws ExecutionException{
		ISelection selection =  window.getActivePage().getSelection();
		if(selection != null && selection instanceof TextSelection) {
			TextSelection userSelectText = (TextSelection)selection;
			return userSelectText.getText().replace("\n", "").trim(); 
		}
		else
			return "";
	}
	
	public IFileEditorInput getCurrentEditorFile() {
		return (IFileEditorInput)window.getActivePage().getActiveEditor().getEditorInput();
	}
	
	public String getCurrentProjectLocation() {
		IFileEditorInput editorFile = getCurrentEditorFile();
		IProject project = editorFile.getFile().getProject();
		return project.getLocation().toString();
	}
	
	public String getCurrentEditorLocation() {
		return getCurrentEditorFile().getFile().getLocation().toString();
	}
	
	public void showMessage(String msg) {
		MessageDialog.openInformation(
			window.getShell(),
			"Robot_framework_refactor_tool",
			msg);
	}
	
	public ShowReferencesView showReferencesView() {
		ShowReferencesView view=null;
		try {
			view= (ShowReferencesView)window.getActivePage().showView("robot_framework_refactor_tool.views.ReferencesView");
		} catch (Exception e) {
			e.printStackTrace();
		}
		return view;
	}
	
	
}
