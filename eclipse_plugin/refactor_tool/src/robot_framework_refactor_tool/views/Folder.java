package robot_framework_refactor_tool.views;

import org.python.core.PyList;

public class Folder extends Node {
	public Folder(Object data) {
		super(data);
	}

	@Override
	public String toString() {
		PyList data = (PyList)this.getData();
		if(data.size() != 0) {
			 return data.get(0).toString();
		}
		return "This is folder";
	}
}
