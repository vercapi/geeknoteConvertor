import unittest

import enmlOutput

import utils


class TestEnmlOutput(unittest.TestCase):
    None

    def testConvertTodoToEvernote(self):
        source = ["*** TODO This is a task"]
        target = ["***<en-todo/> This is a task"]

        result = enmlOutput.convertTodoToEvernote(source)

        self.assertEqual(target, result)

    def testConvertDoneToEvernote(self):
        source = ["*** DONE This is a task done"]
        target = ["***<en-todo checked=\"true\"/> This is a task done"]
        
        result = enmlOutput.convertDoneToEvernote(source)

        self.assertEqual(target, result)

    def testTranslateOrgToHTMLTables(self):

        vSource = ["Some randome text"
                   ,"this is -> something"
                   ,"| id | description |"
                   ,"|----+-------------|"
                   ,"| 1  | text        |"
                   ,"Some other lines * -> Hello"
                   ,"| id | XXxxxxxxxyy |"
                   ,"|----+-------------|"
                   ,"| 3  | None        |"
                   ,"Hellosdlsf. End."]

        vCache = utils.cacheFile(vSource)
        vResult = enmlOutput.translateOrgToHTMLTables(vCache)
    
        vTarget = ["Some randome text", "this is -> something"
                   ,"<TABLE>"
                   ,"<TR><TH>id</TH><TH>description</TH></TR>"
                   ,"<TR><TD>1</TD><TD>text</TD></TR>"
                   ,"</TABLE>"
                   ,"Some other lines * -> Hello"
                   ,"<TABLE>"
                   ,"<TR><TH>id</TH><TH>XXxxxxxxxyy</TH></TR>"
                   ,"<TR><TD>3</TD><TD>None</TD></TR>"
                   ,"</TABLE>"
                   ,"Hellosdlsf. End."
        ]

        self.assertEqual(vResult, vTarget)

    def testConvertToEvernoteLinkNotation(self):
        target = ["[Search](www.google.be)"]
        source = ["[[www.google.be][Search]]"]

        result = enmlOutput.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInText(self):
        target = ["Here is some text and this is [Search](www.google.be) a link"]
        source = ["Here is some text and this is [[www.google.be][Search]] a link"]

        result = enmlOutput.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationDoubleInText(self):
        target = ["Here is some [emacs](www.emacs.org) text and this is [Search](www.google.be) a link"]
        source = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]

        result = enmlOutput.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInTextNoLink(self):
        target = ["Here is some text and this is [Search](www.google.be) a link", "no link"]
        source = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]

        result = enmlOutput.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToGeeknoteTable(self):
        source = ["| Title | test | last |"]
        target = ["Title | test | last"]

        result = enmlOutput.convertToGeeknoteTable(source)

        self.assertEqual(result, target)

    def testConvertToGeeknoteTableHeader(self):
        source = ["|------+----+------|"]
        target = ["---|---|---"]

        result = enmlOutput.convertToGeeknoteTable(source)

        self.assertEqual(result, target)
