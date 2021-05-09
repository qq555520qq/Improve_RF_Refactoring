package robot_framework_refactor_tool.views;

import org.python.core.PyObject;
import org.python.core.PyDictionary;
import org.python.core.PyInteger;

public class Keyword extends Node {
	public Keyword(Object data) {
		super(data);
	}

	@Override
	public String toString() {
		PyObject data = (PyObject)this.getData();
		String keywordLine;
		if (data.getClass() == PyDictionary.class) {
			PyDictionary runKeywords = ((PyDictionary)data);
			keywordLine = ((PyObject)runKeywords.get("keywordName")).__getattr__("lineno").toString();
		}
		else {
			keywordLine = ((PyInteger)(data.__getattr__("lineno"))).toString();
		}
//		­n¥[¤WkeywordName
		String disPlayStr = "Line:" + keywordLine; 

		return disPlayStr;
	}
}
