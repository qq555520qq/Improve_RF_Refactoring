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

public class RefactorHelper extends PythonInterpreter{
	private PyObject refactoringFacade;
	public RefactorHelper(String[] pythonPath) {
		super();
		for(String path:pythonPath)
			importPyPath(path);
		this.exec("from rfrefactoring.refactoringFacade import RefactoringFacade");
		this.refactoringFacade = eval("RefactoringFacade()");
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
	
	public PyObject buildTestData(String path) {
		return this.refactoringFacade.invoke("build", Py.newStringOrUnicode(processPath(path)));
	}
	
	public PyObject getKeyword(PyObject root, String kwName, String testDataSource) {
		return this.refactoringFacade.invoke("get_keyword_obj_from_file",new PyObject[]{root, Py.newStringOrUnicode(kwName), Py.newStringOrUnicode(processPath(testDataSource))});
	}

	public PyObject getVariable(PyObject root, String variableName, String testDataSource) {
		return this.refactoringFacade.invoke("get_variable_obj_from_file", new PyObject[]{root, Py.newStringOrUnicode(variableName), Py.newStringOrUnicode(processPath(testDataSource))});
	}
	
	public PyList getKeywordReferences(PyObject root, PyObject keywordObj) {
		return (PyList)this.refactoringFacade.invoke("get_keyword_references", root, keywordObj);
	}
	
	public PyList getVariableReferences(PyObject root, PyObject variable) {
		return (PyList)this.refactoringFacade.invoke("get_variable_references", root, variable);
	}
	
	public PyList getLocalVariableReferences(PyObject testcaseObj, String variableName) {
		return (PyList)this.refactoringFacade.invoke("get_local_variable_references",testcaseObj, Py.newStringOrUnicode(variableName));
	}
	
	public void renameReferences(List<Node> references, String oldName, String newName) {
		PyList steps = new PyList();
		PyList testDataFiles = new PyList();
		for(Node node:references) {
			if(!node.hasChildren()) {
				steps.add(node.getData());
				Object parentData = node.getParent().getData();
				if(!testDataFiles.contains(parentData))
					testDataFiles.add(parentData);
			}
		}
		this.renameReferencesImpl(steps, oldName, newName);
		this.save(testDataFiles);
	}
	
	public void renameReferencesImpl(PyList references, String oldName, String newName) {
		this.refactoringFacade.invoke("rename_keyword_references", new PyObject[] {references, Py.newStringOrUnicode(oldName), Py.newStringOrUnicode(newName)});
	}
	
	public void renameKeywordDef(PyObject keyword, String newName) {
		this.refactoringFacade.invoke("rename_keyword_def", keyword, Py.newStringOrUnicode(newName));
		set("keyword",keyword);
		this.save(eval("keyword.parent.parent"));
	}
	
	public void renameVariableDef(PyObject variable, String newName) {
		this.refactoringFacade.invoke("rename_variable_def", variable, Py.newStringOrUnicode(newName));
		set("variable", variable);
		this.save(eval("variable.parent.parent"));
	}
	
	public void modifyReference(PyObject reference, String referenceValue) {
		this.refactoringFacade.invoke("modify_reference", reference, Py.newStringOrUnicode(referenceValue));
	}
	
	public void save(PyList testDataFiles) {
		this.refactoringFacade.invoke("save_test_data_files", testDataFiles);
	}
	
	public void save(PyObject testData) {
		this.refactoringFacade.invoke("save", testData);
	}
	
	public String presentKeyword(PyObject keyword) {
		PyString result = (PyString)this.refactoringFacade.invoke("present_keyword",keyword);
		return result.toString();
	}
	
}