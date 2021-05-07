package helper;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

import org.python.core.Py;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import robot_framework_refactor_tool.views.Node;

public class NewRefactorHelper extends PythonInterpreter{
	private PyObject newRefactoringFacade;
	public NewRefactorHelper(String[] pythonPath) {
		super();
		for(String path:pythonPath)
			importPyPath(path);
		this.exec("from rfrefactoring.newRfrefactoring.newRefactoringFacade import NewRefactoringFacade");
		this.newRefactoringFacade = eval("NewRefactoringFacade()");
	}
	
	public static String processPath(String path) {
		Path p = Paths.get(path);
		return p.toString().replace('\\', '/');
	}
	
	public void importPyPath(String pypath) {
		exec("from os import path");
		exec("import sys");
		exec("paths = path.normpath('"+Py.newStringOrUnicode(processPath(pypath))+"')");
		exec("sys.path.append(paths)");
	}
	
	public PyList buildProjectModels(String projectPath) {
		return (PyList)this.newRefactoringFacade.invoke("build_project_models", Py.newStringOrUnicode(processPath(projectPath)));
	}
	
}