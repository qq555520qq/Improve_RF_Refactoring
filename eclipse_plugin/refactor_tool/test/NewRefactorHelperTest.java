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
	private PyObject fileModel;
	@Before
	public void setUp() {
		initNewRefactorHelper();
		this.testDataPath = curDir+"/new_test_data/";
		this.fileModel = this.helper.buildFileModel(this.testDataPath + "test_data.robot");
		this.allModels = this.helper.buildProjectModels(testDataPath);
	}

	@Test
	public void testBuildProjectModels() {
		assertNotEquals(Py.None, this.allModels);
	}

	@Test
	public void testBuildFileModel() {
		assertNotEquals(Py.None, this.fileModel);
	}
	
	@Test
	public void testGetStepsThatWillBeWraped() {
		PyList steps = this.helper.getStepsThatWillBeWraped(this.fileModel, 46, 53);
		assertEquals(3, steps.size());
	}
	
	@Test
	public void testPresentSameSteps() {
		PyList steps = this.helper.getStepsThatWillBeWraped(this.fileModel, 46, 53);
		assertEquals(3, steps.size());
		PyList sameStepsBlocks = this.helper.getSameKeywordsWithSteps(this.allModels, steps);
		String presentText = this.helper.presentSameSteps((PyList)sameStepsBlocks.get(0));
		assertEquals(presentText, "Log    Welcome to taipei\nFor ${var} IN @{testVariable}\n    Log Mutiple Text    ${var}\n    Log Two Different Text    ${var}    new${var}\nEND\n    [Teardown]    Run Keywords    Test Keyword\n    ...    AND    For Loop Keyword    5\n    ...    AND    For Loop Keyword    2\n");
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
