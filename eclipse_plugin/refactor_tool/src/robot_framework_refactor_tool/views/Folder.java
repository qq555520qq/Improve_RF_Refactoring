package robot_framework_refactor_tool.views;

import org.python.core.PyList;
import org.python.core.PyObject;

public class Folder extends Node {
	public Folder(Object data) {
		super(data);
	}

	@Override
	public String toString() {
		PyList data = (PyList) this.getData();
		if (data.size() != 0) {
			for (Object node : data) {
				if(!(PyList.class.isInstance(node))) {
					String filePath = ((PyObject)node).__getattr__("source").toString();
					int index = filePath.lastIndexOf("/");
					String folderPath = filePath.substring(0, index);
					return folderPath;
				}
			}
		}
		return "Folder without file";
	}
}
