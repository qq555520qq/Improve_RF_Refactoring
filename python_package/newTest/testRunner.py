import unittest
from os import path
import sys
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from builder.testModelBuilderTest import TestModelBuilderTest
from keywords.keywordFinderTest import KeywordFinderTest
from keywords.keywordRenamerTest import KeywordRenamerTest
from checker.fileCheckerTest import FileCheckerTest
from keywords.keywordMoveHelperTest import KeywordMoveHelperTest
from keywords.keywordCreatorTest import KeywordCreatorTest

if __name__ == "__main__":
    suite = (unittest.TestLoader().loadTestsFromTestCase(TestModelBuilderTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordFinderTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordRenamerTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(FileCheckerTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordMoveHelperTest))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordCreatorTest))
    unittest.TextTestRunner(verbosity=2).run(suite)
