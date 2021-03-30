import unittest
from os import path
import sys
p = path.normpath(path.dirname(path.abspath(__file__))+"/../..")
sys.path.append(p)
from testModelBuilderTest import TestModelBuilderTest
from keywordFinderTest import KeywordFinderTest
from keywordRenamerTest import KeywordRenamerTest
from fileCheckerTest import FileCheckerTest

if __name__ == "__main__":
    suite = (unittest.TestLoader().loadTestsFromTestCase(KeywordFinderTest))
    # suite = (unittest.TestLoader().loadTestsFromTestCase(TestModelBuilderTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordFinderTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(KeywordRenamerTest))
    # suite.addTest(unittest.TestLoader().loadTestsFromTestCase(FileCheckerTest))
    unittest.TextTestRunner(verbosity=2).run(suite)
