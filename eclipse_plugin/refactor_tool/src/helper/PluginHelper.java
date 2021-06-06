package helper;

import java.awt.Desktop;
import java.io.BufferedReader;
import java.io.File;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
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

import robot_framework_refactor_tool.views.FileSelectionView;
import robot_framework_refactor_tool.views.SameKeywordsSelectionView;
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

	public static NewRefactorHelper getNewRefactorHelper() {
		NewRefactorHelper newRefactorHelper = null;
		String pythonHome = NewRefactorHelper.processPath(PluginHelper.getPythonHome());
		try {
			String jythonPath = NewRefactorHelper.processPath(pythonHome+"/rfrefactoring/jython-standalone-2.7.2b3.jar");
			PluginHelper.initPython(jythonPath, pythonHome);
			newRefactorHelper = new NewRefactorHelper(new String[] {});
		}catch(Exception e) {
			
		}
		return newRefactorHelper;
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
	
	public int getUserSelectionStartLine() throws ExecutionException{
		ISelection selection =  window.getActivePage().getSelection();
		if(selection != null && selection instanceof TextSelection) {
			TextSelection userSelectText = (TextSelection)selection;
			return userSelectText.getStartLine();
		}
		else
			return -1;
	}
	
	public int getUserSelectionEndLine() throws ExecutionException{
		ISelection selection =  window.getActivePage().getSelection();
		if(selection != null && selection instanceof TextSelection) {
			TextSelection userSelectText = (TextSelection)selection;
			return userSelectText.getEndLine();
		}
		else
			return -1;
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
	
	public void showMessage(String title,String msg) {
		MessageDialog.openInformation(window.getShell(), title, msg);
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

	public FileSelectionView fileSelectionView() {
		FileSelectionView view=null;
		try {
			view= (FileSelectionView)window.getActivePage().showView("robot_framework_refactor_tool.views.FileSelectionView");
		} catch (Exception e) {
			e.printStackTrace();
		}
		return view;
	}

	public SameKeywordsSelectionView sameKeywordsSelectionView() {
		SameKeywordsSelectionView view=null;
		try {
			view= (SameKeywordsSelectionView)window.getActivePage().showView("robot_framework_refactor_tool.views.SameKeywordsSelectionView");
		} catch (Exception e) {
			e.printStackTrace();
		}
		return view;
	}
	
	public void openFile(String location) {
		try {
			File file = new File(location);
			if(!Desktop.isDesktopSupported()) {
				System.out.println("not supported");
			}
			else if(file.exists()) {
				Desktop desktop = Desktop.getDesktop();
				desktop.open(file);  
			}
		}catch(Exception e) {
			e.printStackTrace();
		}
	}

	public void runTestCasesAndOpenReport(List<String> testCasesPath) {
		List<String> commands = new ArrayList<>();
		commands.add("python");
		commands.add("-m");
		commands.add("robot");
		commands.add("-d");
		commands.add("outByrfrefactoring");
		for(String testCasePath : testCasesPath) {
			commands.add("\"" + testCasePath + "\"");
		}
		ProcessBuilder runTheTest = new ProcessBuilder(commands);
		try {
			Process process = runTheTest.start();
			BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
			String line;
			while ((line = reader.readLine()) != null) {
				if(line.indexOf("log.html") != -1) {
					String outLocation = line.replace("Log:     ", "");
					this.openFile(outLocation);
					break;
				}
			}
		}catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	
}
