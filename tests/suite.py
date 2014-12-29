import unittest
import glob
import os
import sys

sys.path.append(".")
sys.path.append("./geeknoteConvertor")

def buildTestSuite():
    suite = unittest.TestSuite()
    for testcase in glob.glob('tests/test*.py'):
        modname = os.path.splitext(testcase)[0].replace('/','.')
        module=__import__(modname,{},{},['1'])
        suite.addTest(unittest.TestLoader().loadTestsFromModule(module))
    return suite

def runTests():
    suite = buildTestSuite()
    print('count: '+str(suite.countTestCases()))
    unittest.TextTestRunner().run(suite)

