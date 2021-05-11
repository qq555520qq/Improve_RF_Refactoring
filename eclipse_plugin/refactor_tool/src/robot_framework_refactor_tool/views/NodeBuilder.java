package robot_framework_refactor_tool.views;

import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;

public class NodeBuilder {
	public Node build(PyList references) {
		Node root = new Node();
		for (PyObject reference : references.getArray()) {
			PyDictionary fileRefdict = (PyDictionary) reference;
			PyObject file = fileRefdict.get(new PyString("testdata"));
			PyList fileReferences = (PyList) fileRefdict.get(new PyString("references"));
			Node fileNode = new TestDataFile(file);
			for (PyObject referenceObj : fileReferences.getArray())
				fileNode.addChild(new Step(referenceObj));
			root.addChild(fileNode);
		}
		return root;
	}

	public Node buildForModels(PyList models) {
		Node root = new Folder(models);
		for (int index = 0; index < models.size(); index++) {
			Object node = models.get(index);
			if (PyList.class.isInstance(node)) {
				Node folderData = this.buildForModels((PyList)node);
				root.addChild(folderData);
			}
			else {
				Node model = new Model(node);
				root.addChild(model);
			}
		}
		return root;

	}

	public Node buildForSameKeywords(PyList sameKeywords) {
		Node root = new Node();
		for (int index = 0; index < sameKeywords.size(); index++) {
			PyList sameKeywordsBody = (PyList)(sameKeywords.get(index));
			Node sameStepsBlock = new SameStepsBlock(sameKeywordsBody);
			for (int sameKeywordIndex = 0; sameKeywordIndex < sameKeywordsBody.size(); sameKeywordIndex++) {
				PyDictionary keywordNode = (PyDictionary)sameKeywordsBody.get(sameKeywordIndex);
				Node keyword = null;
				PyString nodeClass = (PyString)((PyObject)keywordNode.get("node")).__getattr__("__class__").__getattr__("__name__");
				if((String)nodeClass.__tojava__(String.class) == "KeywordCall") {
					keyword = new Keyword(keywordNode.get("node"));
				}
				else {
					keyword = new Keyword(keywordNode.get("keyword"));
				}
				sameStepsBlock.addChild(keyword);
			}
			root.addChild(sameStepsBlock);
		}
		return root;

	}
}
