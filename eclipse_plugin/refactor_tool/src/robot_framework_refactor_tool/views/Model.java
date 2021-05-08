package robot_framework_refactor_tool.views;

import org.python.core.PyObject;

public class Model extends Node {
	public Model(Object data) {
		super(data);
	}

	@Override
	public String toString() {
		PyObject data = (PyObject)this.getData();
		return data.__getattr__("source").toString().replace("\n", "    ");
	}
}
