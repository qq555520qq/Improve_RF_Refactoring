package robot_framework_refactor_tool.views;

import org.python.core.PyDictionary;
import org.python.core.PyObject;
import org.python.core.PyList;

public class SameStepsBlock extends Node {
	public SameStepsBlock(Object data) {
		super(data);
	}

	@Override
	public String toString() {
		PyDictionary data = (PyDictionary)((PyList)this.getData()).get(0);
		PyObject modelWithSameKeywords = (PyObject)data.get("model");
		return modelWithSameKeywords.__getattr__("source").toString().replace("\n", "    ");
	}
}
