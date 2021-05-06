package robot_framework_refactor_tool.views;

import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;

public class NodeBuilder {
	public Node build(PyList references){
		Node root = new Node();
		for(PyObject reference:references.getArray()) {
			PyDictionary fileRefdict = (PyDictionary)reference;
			PyObject file = fileRefdict.get(new PyString("testdata"));
			PyList fileReferences = (PyList)fileRefdict.get(new PyString("references"));
			Node fileNode = new TestDataFile(file);
			for (PyObject referenceObj:fileReferences.getArray()) 
				fileNode.addChild(new Step(referenceObj));
			root.addChild(fileNode);
			}
		return root;
	}
}
