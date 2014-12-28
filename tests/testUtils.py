import unittest
import sys
sys.path.append("../geeknoteConvertor")

import re
import utils
from utils import CacheLocation

class TestUtils(unittest.TestCase):

    def testCached(self):
        vSource = "aaaa"
        vTarget = list("bbbb")

        @utils.cached
        def cacheChecker(pTestList):
            self.assertEqual(pTestList, 'a') #check to see if we get an element of a string converted to a list
            return 'b'

        vResult = cacheChecker(vSource)
        self.assertEqual(vResult, vTarget) # check to see if we get all the values back as one list

    def testRegexrepl(self):
        vSource = "this is a target"
        vString = "ReplacedTarget"
        vTarget = "this is a ReplacedTarget"

        @utils.regexrepl
        def regexreplChecker(pLine):
            return re.subn(r'target', vString, pLine)

        vResult = regexreplChecker(vSource)
        self.assertEqual(vTarget, vResult)

    def testRegexreplMis(self):
        vSource = "this is a target"

        @utils.regexrepl
        def regexreplChecker(pLine):
            return re.subn(r'notarget', 'anything', pLine)

        vResult = regexreplChecker(vSource)
        self.assertEqual(vSource, vResult)

    def testCacheFile(self):
        vSource = ["Hello", "second line"]
        vTarget = ["Hello", "second line"]

        vResult = utils.cacheFile(vSource)

        self.assertEqual(vTarget, vResult)
        
    def testCacheLocationCmpEquals(self):
        targetA = CacheLocation(9,7)
        targetB = CacheLocation(9,7)
        
        self.assertTrue(targetA == targetB) 

    def testCacheLocationCmpSmallerLines(self):
        targetA = CacheLocation(9,7)
        targetB = CacheLocation(10,7)
        
        self.assertTrue(targetA < targetB) 

    def testCacheLocationCmpBiggerLines(self):
        targetA = CacheLocation(9,7)
        targetB = CacheLocation(6,7)
        
        self.assertTrue(targetA > targetB) 

    def testCacheLocationCmpSmallerIndex(self):
        targetA = CacheLocation(9,6)
        targetB = CacheLocation(9,7)
        
        self.assertTrue(targetA < targetB) 

    def testCacheLocationCmpBiggerIndex(self):
        targetA = CacheLocation(9,11)
        targetB = CacheLocation(9,8)
        
        self.assertTrue(targetA > targetB) 


    def testCacheLocationCmpSmallerOrEqualsIndex(self):
        targetA = CacheLocation(9,6)
        targetB = CacheLocation(9,7)
        
        self.assertTrue(targetA <= targetB) 

    def testCacheLocationCmpBiggerOrEqualsIndex(self):
        targetA = CacheLocation(9,11)
        targetB = CacheLocation(9,8)
        
        self.assertTrue(targetA >= targetB) 

    def testCacheLocationCmpSmallerOrEqualsEqualsIndex(self):
        targetA = CacheLocation(9,7)
        targetB = CacheLocation(9,7)
        
        self.assertTrue(targetA <= targetB) 

    def testCacheLocationCmpBiggerOrEqualsEqualsIndex(self):
        targetA = CacheLocation(9,11)
        targetB = CacheLocation(9,11)
        
        self.assertTrue(targetA >= targetB) 

    def testGetCacheLocation(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = [" 1", "Word"]

        vCacheLocationStart = CacheLocation(1,4)
        vCacheLocationEnd = CacheLocation(2,4)
        vResult = CacheLocation.getCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocation(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "My", "Text", "Last"]

        vReplacement = ["My", "Text"]

        vCacheLocationStart = CacheLocation(1,0)
        vCacheLocationEnd = CacheLocation(2,6)
        vResult = CacheLocation.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocationWithin(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "Line My", "Text L", "Last"]

        vReplacement = ["My", "Text"]

        vCacheLocationStart = CacheLocation(1,5)
        vCacheLocationEnd = CacheLocation(2,4)
        vResult = CacheLocation.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocationDifirence(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "Line My", "Own", "Text L", "Last"]

        vReplacement = ["My", "Own", "Text"]

        vCacheLocationStart = CacheLocation(1,5)
        vCacheLocationEnd = CacheLocation(2,4)
        vResult = CacheLocation.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)
