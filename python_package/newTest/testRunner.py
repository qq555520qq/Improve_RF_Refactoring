import unittest
from os import path
import sys
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from testModelBuilderTest import TestModelBuilderTest
from keywordFinderTest import KeywordFinderTest
from keywordRenamerTest import KeywordRenamerTest
from fileCheckerTest import FileCheckerTest
from keywordMoveHelperTest import KeywordMoveHelperTest
from keywordCreatorTest import KeywordCreatorTest

if __name__ == "__main__":
    suite = (unittest.TestLoader().loadTestsFromTestCase(KeywordCreatorTest))
    # suite = (unittest.TestLoader().loadTestsFromTestCase(TestModelBuilderTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordFinderTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordRenamerTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(FileCheckerTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordMoveHelperTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordCreatorTest))
    unittest.TextTestRunner(verbosity=2).run(suite)
