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
import helper.RefactorHelper;
public class RefactorHelperTest {
	private String curDir;
	private String testDataPath;
	private RefactorHelper helper;
	private PyObject testDataRoot;
	@Before
	public void setUp() {
		initRefactorHelper();
		this.testDataPath = curDir+"/test_data/";
		testDataRoot = helper.buildTestData(testDataPath);
	}
	
	@After
	public void tearDown(){
		this.helper.close();
	}
	
	@Test
	public void testGetUserSelectKeyword(){
		String userTestData = testDataPath+"/ezScrum.txt";
		String userSelectKeyword = "Login EzScrum";
		PyObject keyword = helper.getKeyword(this.testDataRoot, userSelectKeyword, userTestData);
		String actualKeywordName = keyword.__getattr__("name").toString();
		assertEquals(userSelectKeyword, actualKeywordName);	
	}
	
	@Test
	public void testGetUserSelectVariable() {
		String userTestData = testDataPath+"/testResource.txt";
		String userSelectVariable = "${resourceFileVariable}";
		PyObject variable = helper.getVariable(testDataRoot, userSelectVariable, userTestData);
		assertNotEquals(Py.None, variable);
		String actualValue = ((PyList)variable.__getattr__("value")).get(0).toString();
		assertEquals("resource file test data", actualValue);
	}
	
	@Test
	public void testGetCommonKeywordReferences() {
		String userTestData = testDataPath+"/ezScrum.txt";
		String userSelectKeyword = "Login EzScrum";
		PyObject keyword = helper.getKeyword(this.testDataRoot, userSelectKeyword, userTestData);
		PyList references = helper.getKeywordReferences(this.testDataRoot, keyword);
		assertEquals(4, references.size());
	}
	
	@Test
	public void testGetSelfKeywordReferences() {
		String testData = testDataPath+"/add sprint.robot";
		String userSelectKeyword = "Choose Project";
		PyObject keyword = helper.getKeyword(this.testDataRoot, userSelectKeyword, testData);
		PyList references = helper.getKeywordReferences(testDataRoot, keyword);
		assertEquals(1, references.size());
		PyDictionary testDataReference = (PyDictionary)references.getArray()[0];
		PyList referencesData = (PyList)testDataReference.get(new PyString("references"));
		PyObject referencesFile = testDataReference.get(new PyString("testdata"));
		assertEquals(2, referencesData.size());
		assertEquals(Paths.get(testData).toAbsolutePath().toString(), Paths.get(referencesFile.__getattr__("source").toString()).toAbsolutePath().toString());	
	}
	
	@Test
	public void testGetSelfVariableReferences() {
		String testData = testDataPath+"/add story by excel.robot";
		String variableName = "${StoryPath}";
		PyObject variable = this.helper.getVariable(testDataRoot, variableName, testData);
		assertNotEquals(Py.None, variable);
		PyList references = helper.getVariableReferences(testDataRoot, variable);
		assertEquals(1, references.size());
		PyDictionary testDataReferences = (PyDictionary)references.get(0);
		PyList referencesData = (PyList)testDataReferences.get(new PyString("references"));
		assertEquals(3, referencesData.size());
	}
	
	@Test
	public void testGetCommonVariableReferences() {
		String testData = testDataPath+"/testResource.txt";
		String variableName = "${resourceFileVariable}";
		PyObject variable = this.helper.getVariable(testDataRoot, variableName, testData);
		assertNotEquals(Py.None, variable);
		PyList references = helper.getVariableReferences(testDataRoot, variable);
		assertEquals(1, references.size());
	}
	
	@Test
	public void testWithUnicodeProject(){
		String userTestData = testDataPath+"/中文路徑/ezScrum.txt";
		String userSelectKeyword = "Login EzScrum";
		PyObject keyword = helper.getKeyword(this.testDataRoot, userSelectKeyword, userTestData);
		String actualKeywordName = keyword.__getattr__("name").toString();
		assertEquals(userSelectKeyword, actualKeywordName);	
	}
	
	public void initRefactorHelper() {
		//pythonSite is the site-packages path, you should replace it with yours.
		String pythonSite = "C:\\Program Files\\Python36\\Lib\\site-packages";
		String jythonPath = pythonSite+"/rfrefactoring/jython-standalone-2.7.2b3.jar";
		PluginHelper.initPython(jythonPath, pythonSite);
		this.curDir = System.getProperty("user.dir");
		this.helper = new RefactorHelper(new String[] {});
	}
	
}
