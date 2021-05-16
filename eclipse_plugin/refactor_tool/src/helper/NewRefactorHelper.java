package helper;

import java.nio.file.Path;
import java.nio.file.Paths;

import org.python.core.Py;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;


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

	public PyList buildTokensOfArgumentsInNewKeyword(PyList newArgs) {
		return (PyList)this.newRefactoringFacade.invoke("build_tokens_of_arguments_in_new_keyword", newArgs);
	}

	public PyList getNewKeywordBodyWithStepsAndNewArguments(PyList steps,PyList newArgsTokens) {
		return (PyList)this.newRefactoringFacade.invoke("get_new_keyword_body_with_steps_and_new_arguments", steps, newArgsTokens);
	}

	public void createNewKeywordForFile(String filePath, String newKeywordName, PyList newKeywordBody) {
		this.newRefactoringFacade.invoke("create_new_keyword_for_file", new PyObject[]{Py.newStringOrUnicode(processPath(filePath)), Py.newStringOrUnicode(newKeywordName), newKeywordBody});
	}

	public PyObject replaceStepsWithKeywordAndGetModelsWithReplacing(String keywordName, PyList keywordArgs, PyList steps) {
		return this.newRefactoringFacade.invoke("replace_steps_with_keyword_and_get_models_with_replacing", new PyObject[] {Py.newStringOrUnicode(keywordName), keywordArgs, steps});
	}

	public PyList getModelsWithoutImportingNewResourceFromModelsWithReplacement(String newKeywordName, PyList modelsWithReplacement, String newKeywordPath) {
		return (PyList) this.newRefactoringFacade.invoke("get_models_without_importing_new_resource_from_models_with_replacement", new PyObject[]{Py.newStringOrUnicode(newKeywordName), modelsWithReplacement, Py.newStringOrUnicode(processPath(newKeywordPath))});
	}
	
	public String presentSameSteps(PyList sameStepsBlock) {
		PyString result = (PyString)this.newRefactoringFacade.invoke("present_same_steps", sameStepsBlock);
		return result.toString();
	}
	
	public void importNewResourceForModelWithoutImporting(PyObject model, String resourceValue) {
		this.newRefactoringFacade.invoke("import_new_resource_for_model_without_importing", model, Py.newStringOrUnicode(resourceValue));
	}
	
	public PyObject getMovedKeywordNodeFromModel(PyObject model, String keywordName, int keywordLine) {
		return this.newRefactoringFacade.invoke("get_moved_keyword_node_from_model", new PyObject[]{model, Py.newStringOrUnicode(keywordName), Py.newInteger(keywordLine)});
	}

	public void removeDefinedKeyword(PyObject model, PyObject keywordNode) {
		this.newRefactoringFacade.invoke("remove_defined_keyword", model, keywordNode);
	}

	public void insertDefinedKeyword(PyObject model, PyObject keywordNode) {
		this.newRefactoringFacade.invoke("insert_defined_keyword", model, keywordNode);
	}

	public PyList getModelsUsingKeyword(String pathOfKeywordDefined, String keywordName) {
		return (PyList)this.newRefactoringFacade.invoke("get_models_using_keyword", new PyObject[] {Py.newStringOrUnicode(processPath(pathOfKeywordDefined)), Py.newStringOrUnicode(keywordName)});
	}
	
	public PyList getModelsWithoutImportTargetResource(String movedKeywordName, String fromFilePath, String targetFilePath) {
		return (PyList) this.newRefactoringFacade.invoke("get_models_without_import_target_resource", new PyObject[] {Py.newStringOrUnicode(movedKeywordName), Py.newStringOrUnicode(fromFilePath), Py.newStringOrUnicode(targetFilePath)});
	}

	public void saveModels(PyList models) {
		this.newRefactoringFacade.invoke("save_models", models);
	}

	public PyList getVariablesNotDefinedInSteps(PyList steps) {
		return (PyList)this.newRefactoringFacade.invoke("get_variables_not_defined_in_steps", steps);
	}
}