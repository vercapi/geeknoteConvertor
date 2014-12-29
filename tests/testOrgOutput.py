import unittest

import orgOutput

class TestOrgOuput(unittest.TestCase):

    def testCompleteOrgTableNotation(self):
        source = ["Command  |  Key  |  Description"]
        target = ["|Command  |  Key  |  Description|"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationLeading(self):
        source = ["|Command  |  Key  |  Description"]
        target = ["|Command  |  Key  |  Description|"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationTrailing(self):
        source = ["Command  |  Key  |  Description|"]
        target = ["|Command  |  Key  |  Description|"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationBoth(self):
        source = ["|Command  |  Key  |  Description|"]
        target = ["|Command  |  Key  |  Description|"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationNoLine(self):
        source = ["This is a normal line"]
        target = ["This is a normal line"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationHeader(self):
        source = ["---|---|---"]
        target = ["|---+---+---|"]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationEmptyLine(self):
        source = ["|Command  |  Key  |  Description", "", "|Test | A | nothing", ""]
        target = ["|Command  |  Key  |  Description|", "|Test | A | nothing|", ""]

        result = orgOutput.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotation(self):
        target = ["[[www.google.be][Search]]"]
        source = ["[Search](www.google.be)"]

        result = orgOutput.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInText(self):
        target = ["Here is some text and this is [[www.google.be][Search]] a link"]
        source = ["Here is some text and this is [Search](www.google.be) a link"]

        result = orgOutput.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationDoubleInText(self):
        target = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]
        source = ["Here is some [emacs](www.emacs.org) text and this is [Search](www.google.be) a link"]

        result = orgOutput.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInTextNoLink(self):
        target = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]
        source = ["Here is some text and this is [Search](www.google.be) a link", "no link"]

        result = orgOutput.convertToOrgLinkNotation(source)
        
        self.assertEqual(result, target)

    def testConvertTodoToOrg(self):
        target = ["*** TODO This is a task"]
        source = ["***<en-todo/> This is a task"]

        result = orgOutput.convertTodoToOrg(source)

        self.assertEqual(target, result)

    def testConvertDoneToOrg(self):
        target = ["*** DONE This is a task done"]
        source = ["***<en-todo checked=\"true\"/> This is a task done"]

        result = orgOutput.convertDoneToOrg(source)

        self.assertEqual(target, result)    
