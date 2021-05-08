import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotEquals;

import java.nio.file.Paths;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.python.core.Py;
import org.python.core.PyDictionary;
import org.python.core.PyList;
import org.python.core.PyObject;
import org.python.core.PyString;

import helper.PluginHelper;
import helper.NewRefactorHelper;

public class NewRefactorHelperTest {
	private String curDir;
	private String testDataPath;
	private NewRefactorHelper helper;
	private PyList allModels;
	@Before
	public void setUp() {
		initNewRefactorHelper();
		this.testDataPath = curDir+"/new_test_data/";
	}

	@Test
	public void testBuildProjectModels() {
		this.allModels = this.helper.buildProjectModels(testDataPath);
		assertNotEquals(Py.None, this.allModels);
	}

	@Test
	public void testBuildFileModel() {
		PyObject fileModel = this.helper.buildFileModel(this.testDataPath + "test_data.robot");
		assertNotEquals(Py.None, fileModel);
	}
	
	@Test
	public void testGetStepsThatWillBeWraped() {
		PyObject fileModel = this.helper.buildFileModel(this.testDataPath + "test_data.robot");
		PyList steps = this.helper.getStepsThatWillBeWraped(fileModel, 46, 53);
		assertEquals(3, steps.size());
	}

	public void initNewRefactorHelper() {
		//pythonSite is the site-packages path, you should replace it with yours.
		String pythonSite = "C:\\Program Files\\Python36\\Lib\\site-packages";
		String jythonPath = pythonSite+"/rfrefactoring/jython-standalone-2.7.2b3.jar";
		PluginHelper.initPython(jythonPath, pythonSite);
		this.curDir = System.getProperty("user.dir");
		this.helper = new NewRefactorHelper(new String[] {});
	}
	
}
