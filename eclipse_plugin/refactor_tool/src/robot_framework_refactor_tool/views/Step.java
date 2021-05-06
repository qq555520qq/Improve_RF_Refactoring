package robot_framework_refactor_tool.views;

import org.python.core.PyObject;

public class Step extends Node {
	public Step(Object data) {
		super(data);
	}
	@Override
	public String toString() {
		PyObject data = (PyObject)this.getData();
		return data.invoke("get_present_value").toString().replace("\n", "    ");
	}
}
