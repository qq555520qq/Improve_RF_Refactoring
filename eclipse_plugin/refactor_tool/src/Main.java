import org.eclipse.swt.widgets.*;
import org.python.core.PyObject;

import robot_framework_refactor_tool.views.ChangeSignatureDialog;
import helper.PluginHelper;
import helper.RefactorHelper;
public class Main {

	public static void main(String[] args) {
		RefactorHelper helper=null;
		try {
			String source = "C:\\Users\\lab1321\\Documents\\workspace\\thesisTest\\Amazon Change Language.robot";
			String jythonPath = RefactorHelper.processPath("C:\\jython2.7.2\\bin");
			String sitePath = RefactorHelper.processPath("C:\\Users\\lab1321\\AppData\\Local\\Programs\\Python\\Python37\\Lib\\site-packages");
			PluginHelper.initPython(jythonPath, sitePath);
			helper = new RefactorHelper(new String[] {});
			PyObject root = helper.buildTestData(source);
			PyObject keyword = helper.getKeyword(root, "Change Language", source);
			Display display = new Display();
			Shell shell = new Shell(display);
			ChangeSignatureDialog dialog = new ChangeSignatureDialog(shell, helper, keyword);
			dialog.open();
			
			// TODO Auto-generated method stub
		}catch(Exception e){
			e.printStackTrace();
		}
		finally {
			helper.close();
		}
	}

}
