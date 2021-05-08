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

	public PyObject buildFileModel(String filePath) {
		return this.newRefactoringFacade.invoke("build_file_model", Py.newStringOrUnicode(processPath(filePath)));
	}

	public PyList getStepsThatWillBeWraped(PyObject fromModel, int startLine, int endLine) {
		return (PyList)this.newRefactoringFacade.invoke("get_steps_that_will_be_wraped", new PyObject[] {fromModel, Py.newInteger(startLine), Py.newInteger(endLine)});
	}

	public PyList getSameKeywordsWithSteps(PyList allModels, PyList steps) {
		return (PyList)this.newRefactoringFacade.invoke("get_same_keywords_with_steps", allModels, steps);
	}

	public PyObject getStepFromStepsByLine(PyList steps, int line) {
		return this.newRefactoringFacade.invoke("get_step_from_steps_by_line", steps, Py.newInteger(line));
	}

	public PyList getArgumentsFromStep(PyObject step) {
		return (PyList)this.newRefactoringFacade.invoke("get_arguments_from_step", step);
	}

	public void updateArgumentsOfStep(PyList steps, PyObject step, PyList argsOfStep, String updatedArgIndex, String newArg) {
		this.newRefactoringFacade.invoke("update_arguments_of_step", new PyObject[] {steps, step, argsOfStep, Py.newStringOrUnicode(processPath(updatedArgIndex)), Py.newStringOrUnicode(processPath(newArg))});
	}

	public PyList buildTokensOfArgumentsInNewKeyword(PyList newArgs) {
		return (PyList)this.newRefactoringFacade.invoke("build_tokens_of_arguments_in_new_keyword", newArgs);
	}

	public PyList getNewKeywordBodyWithStepsAndNewArguments(PyList steps,PyList newArgsTokens) {
		return (PyList)this.newRefactoringFacade.invoke("get_new_keyword_body_with_steps_and_new_arguments", steps, newArgsTokens);
	}

	public void createNewKeywordForFile(String filePath, String newKeywordName, PyList newKeywordBody) {
		this.newRefactoringFacade.invoke("create_new_keyword_for_file", new PyObject[]{Py.newStringOrUnicode(processPath(filePath)), Py.newStringOrUnicode(processPath(newKeywordName)), newKeywordBody});
	}

	public PyObject replaceStepsWithKeywordAndGetModelsWithReplacing(String keywordName, PyList keywordArgs, PyList steps) {
		return this.newRefactoringFacade.invoke("replace_steps_with_keyword_and_get_models_with_replacing", new PyObject[]{Py.newStringOrUnicode(processPath(keywordName)), keywordArgs, steps});
	}

	public PyList getModelsWithoutImportingNewResourceFromModelsWithReplacement(String newKeywordName, PyList modelsWithReplacement, String newKeywordPath) {
		return (PyList) this.newRefactoringFacade.invoke("get_models_without_importing_new_resource_from_models_with_replacement", new PyObject[]{Py.newStringOrUnicode(processPath(newKeywordName)), modelsWithReplacement, Py.newStringOrUnicode(processPath(newKeywordPath))});
	}
	
	public void importNewResourceForModelWithoutImporting(PyObject model, String resourceValue) {
		this.newRefactoringFacade.invoke("import_new_resource_for_model_without_importing", model, Py.newStringOrUnicode(processPath(resourceValue)));
	}
	
	public PyObject getMovedKeywordNodeFromModel(PyObject model, String keywordName) {
		return this.newRefactoringFacade.invoke("get_moved_keyword_node_from_model", model, Py.newStringOrUnicode(processPath(keywordName)));
	}

	public void removeDefinedKeyword(PyObject model, PyObject keywordNode) {
		this.newRefactoringFacade.invoke("remove_defined_keyword", model, keywordNode);
	}

	public void insertDefinedKeyword(PyObject model, PyObject keywordNode) {
		this.newRefactoringFacade.invoke("insert_defined_keyword", model, keywordNode);
	}
	
}