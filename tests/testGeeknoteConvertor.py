import sys
sys.path.append("../geeknoteConvertor")

import geeknoteConvertorLib
import unittest

class TestGeeknoteConvertor(unittest.TestCase):
    
    def test_replaceChar(self):
        source = "* this is a bulletpoint"
        target = "# this is a bulletpoint"

        result = geeknoteConvertorLib.replaceChar(source, "*", "#")
        self.assertEqual(target, result)

    def test_replaceCharMutliple(self):
        source = "** this is a bulletpoint"
        target = "## this is a bulletpoint"

        result = geeknoteConvertorLib.replaceChar(source, "*", "#")
        self.assertEqual(target, result)

    def test_escapeChars(self):
        source = " # just something _ I'm writing"
        target = " \# just something \_ I'm writing"
        
        result = geeknoteConvertorLib.escapeChars(source, ["#", "_"])
        self.assertEqual(target, result)

    def test_escapeCharsMutliple(self):
        source = " # just something __ I'm writing"
        target = " \# just something \_\_ I'm writing"
        
        result = geeknoteConvertorLib.escapeChars(source, ["#", "_"])
        self.assertEqual(target, result)

    def test_escapeCharsFile(self):
        source = ["# test", "_ test"]
        target = ["\\# test", "\\_ test"]
        
        result = geeknoteConvertorLib.escapeCharsFile(source, ["#", "_"])
        self.assertEqual(target, result)

    def test_replaceCharFile(self):
        source = ["# test", "_ test"]
        target = ["* test", "_ test"]
        
        result = geeknoteConvertorLib.replaceCharFile(source, "#", "*")
        self.assertEqual(target, result)

    def test_replaceEscapedChar(self):
        source = "\\* this is a bulletpoint"
        target = "* this is a bulletpoint"

        result = geeknoteConvertorLib.replaceChar(source, "\\*", "*")
        self.assertEqual(target, result)

    def test_unsecapeChar(self):
        source = "\* this is a bulletpoint"
        target = "* this is a bulletpoint"

        result = geeknoteConvertorLib.unescapeChars(source, ["\*", "*"])
        self.assertEqual(target, result)

    def testReadTableTag(self):
        source = "azeazee <table> som things </table>"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()

        self.assertIsNotNone(table)
    
    def testGetNumOfRows(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        self.assertEqual(2, table.getRows())

    def testGetNumOfCols(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        self.assertEqual(2, table.getCols(0))
        self.assertEqual(2, table.getCols(1))

    def testGetNumOfCols(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"
        target = [["id", "description"], ["1", "text"]]

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        self.assertEqual(target, table.getTable())

    def testGetColumnSize(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        self.assertEqual(11, table.getColumnSize(1))

    def testGetColumnContent(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        self.assertEqual("1", table.getColumnContent(0,1))

    def testPrintColumn(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"
        target = " text        |"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        orgWriter = geeknoteConvertorLib.OrgWriter(table)
        result = orgWriter.printColumn(1, 1)
        self.assertEqual(target, result)

    def testPrintRow(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"
        target = "| 1  | text        |\n"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        orgWriter = geeknoteConvertorLib.OrgWriter(table)
        result = orgWriter.printRow(1)
        self.assertEqual(target, result)

    def testPrintSeparator(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"
        target = "|----+-------------|\n"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        orgWriter = geeknoteConvertorLib.OrgWriter(table)
        result = orgWriter.printSeparatorLine()
        self.assertEqual(target, result)

    def testPrint(self):
        source = "<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>"
        target =  "|----+-------------|\n"
        target += "| id | description |\n"
        target += "|----+-------------|\n"
        target += "| 1  | text        |\n"
        target += "|----+-------------|\n"

        parser = geeknoteConvertorLib.OrgHTMLParser()
        parser.feed(source)

        table = parser.getTable()
        
        orgWriter = geeknoteConvertorLib.OrgWriter(table)
        result = orgWriter.generate()
        self.assertEqual(target, result)                

    def testFindTableStart(self):
        source = ["kjsqklfjmqsdf sdf<table>","klsdkfjlsdf<ld/> sdfs","f</table>qsdqsd<table></table>"]
        
        expected = geeknoteConvertorLib.CacheLocation(0, 17)

        start = geeknoteConvertorLib.CacheLocation(0,0)
        result = geeknoteConvertorLib.OrgHTMLParser.findTableStart(start, source)
        self.assertEqual(expected, result)


    def testFindTableEnd(self):
        source = ["kjsqklfjmqsdf sdf<table>","klsdkfjlsdf<ld/> sdfs","f</table>qsdqsd<table></table>"]
        
        expected = geeknoteConvertorLib.CacheLocation(2, 8)

        start = geeknoteConvertorLib.CacheLocation(0,0)
        start = geeknoteConvertorLib.OrgHTMLParser.findTableStart(start, source)
        result = geeknoteConvertorLib.OrgHTMLParser.findTableEnd(start, source)
        self.assertEqual(expected, result)

    def testFindTableEndFormatMess(self):
        source = ["kjsqklfjmqsdf</table> sdf<table></table>","klsdkfjlsdf<ld/> sdfs","f</table>qsdqsd<table></table>"]
        
        expected = geeknoteConvertorLib.CacheLocation(0, 39)

        start = geeknoteConvertorLib.CacheLocation(0,0)
        start = geeknoteConvertorLib.OrgHTMLParser.findTableStart(start, source)
        result = geeknoteConvertorLib.OrgHTMLParser.findTableEnd(start, source)
        self.assertEqual(expected, result)

    def testCacheLocationCmpEquals(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,7)
        targetB = geeknoteConvertorLib.CacheLocation(9,7)
        
        self.assertTrue(targetA == targetB) 

    def testCacheLocationCmpSmallerLines(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,7)
        targetB = geeknoteConvertorLib.CacheLocation(10,7)
        
        self.assertTrue(targetA < targetB) 

    def testCacheLocationCmpBiggerLines(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,7)
        targetB = geeknoteConvertorLib.CacheLocation(6,7)
        
        self.assertTrue(targetA > targetB) 

    def testCacheLocationCmpSmallerIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,6)
        targetB = geeknoteConvertorLib.CacheLocation(9,7)
        
        self.assertTrue(targetA < targetB) 

    def testCacheLocationCmpBiggerIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,11)
        targetB = geeknoteConvertorLib.CacheLocation(9,8)
        
        self.assertTrue(targetA > targetB) 


    def testCacheLocationCmpSmallerOrEqualsIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,6)
        targetB = geeknoteConvertorLib.CacheLocation(9,7)
        
        self.assertTrue(targetA <= targetB) 

    def testCacheLocationCmpBiggerOrEqualsIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,11)
        targetB = geeknoteConvertorLib.CacheLocation(9,8)
        
        self.assertTrue(targetA >= targetB) 

    def testCacheLocationCmpSmallerOrEqualsEqualsIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,7)
        targetB = geeknoteConvertorLib.CacheLocation(9,7)
        
        self.assertTrue(targetA <= targetB) 

    def testCacheLocationCmpBiggerOrEqualsEqualsIndex(self):
        targetA = geeknoteConvertorLib.CacheLocation(9,11)
        targetB = geeknoteConvertorLib.CacheLocation(9,11)
        
        self.assertTrue(targetA >= targetB) 

    def testReplaceTables(self):
        #TODO: Source needs to be real tables, see comments below
        source = ["bvnbvnvnbvn qsdqsdqd<table><tr><th>id</th><th>description</th></tr><tr><td>1</td><td>text</td></tr></table>","azeaeezaeae<ld/> sdfs","iopiipippp></p>"]
        
        target = ["bvnbvnvnbvn qsdqsdqd"]

        targetStr =  "|----+-------------|\n"
        targetStr += "| id | description |\n"
        targetStr += "|----+-------------|\n"
        targetStr += "| 1  | text        |\n"
        targetStr += "|----+-------------|\n"
        target += targetStr.splitlines()
        target += ["azeaeezaeae<ld/> sdfs","iopiipippp></p>"]

        result = geeknoteConvertorLib.replaceTables(source)


        self.assertEqual(target, result)

    def testCleanHTML(self):
        source = ["<div kljsdlksjf","lksdfmlksdf", "</div>","</div>","This is the actual file"]
        target = source[4:]

        result = geeknoteConvertorLib.removeHeader(source)

        self.assertEqual(result, target)

    def testRemoveEmptyLines(self):
        source = ["\n","","     ","\n", " ", "First Line", ""]
        target = ["First Line", ""]

        result = geeknoteConvertorLib.removeEmptyLines(source)

        self.assertEqual(result, target)

    def testOnlyEmptyLines(self):
        source = ["\n","","     ","\n", " ", "   \n", ""]
        target = []

        result = geeknoteConvertorLib.removeEmptyLines(source)

        self.assertEqual(result, target)        

    def testENMLcleanOrgHTMLTable(self):
        source = ["<table border=\"2\" cellspacing=\"0\" cellpadding=\"6\" rules=\"groups\" frame=\"hsides\">"]
        target = ["<table border=\"2\" cellspacing=\"0\" cellpadding=\"6\" rules=\"groups\" >"]

        result = geeknoteConvertorLib.HTMLToENML.removeHtmlAttribute(source, "frame")

        self.assertEqual(result, target)

    def testENMLcleanOrgHTMLTable2(self):
        source = ["<table border=\"2\" cellspacing=\"0\" cellpadding=\"6\" rules=\"groups\" frame=\"hsides\">"]
        target = ["<table border=\"2\" cellspacing=\"0\" cellpadding=\"6\"  frame=\"hsides\">"]

        result = geeknoteConvertorLib.HTMLToENML.removeHtmlAttribute(source, "rules")

        self.assertEqual(result, target)        

    def testCompleteOrgTableNotation(self):
        source = ["Command  |  Key  |  Description"]
        target = ["|Command  |  Key  |  Description|"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationLeading(self):
        source = ["|Command  |  Key  |  Description"]
        target = ["|Command  |  Key  |  Description|"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationTrailing(self):
        source = ["Command  |  Key  |  Description|"]
        target = ["|Command  |  Key  |  Description|"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationBoth(self):
        source = ["|Command  |  Key  |  Description|"]
        target = ["|Command  |  Key  |  Description|"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationNoLine(self):
        source = ["This is a normal line"]
        target = ["This is a normal line"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)

    def testCompleteOrgTableNotationHeader(self):
        source = ["---|---|---"]
        target = ["|---+---+---|"]

        result = geeknoteConvertorLib.completeOrgTableNotation(source)

        self.assertEqual(result, target)


    def testConvertToOrgLinkNotation(self):
        source = ["[[www.google.be][Search]]"]
        target = ["[Search](www.google.be)"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInText(self):
        source = ["Here is some text and this is [[www.google.be][Search]] a link"]
        target = ["Here is some text and this is [Search](www.google.be) a link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationDoubleInText(self):
        source = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]
        target = ["Here is some [emacs](www.emacs.org) text and this is [Search](www.google.be) a link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInTextNoLink(self):
        source = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]
        target = ["Here is some text and this is [Search](www.google.be) a link", "no link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotation(self):
        source = ["[Search](www.google.be)"]
        target = ["[[www.google.be][Search]]"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInText(self):
        source = ["Here is some text and this is [Search](www.google.be) a link"]
        target = ["Here is some text and this is [[www.google.be][Search]] a link"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationDoubleInText(self):
        source = ["Here is some [emacs](www.emacs.org) text and this is [Search](www.google.be) a link"]
        target = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInTextNoLink(self):
        source = ["Here is some text and this is [Search](www.google.be) a link", "no link"]
        target = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToGeeknoteTable(self):
        source = ["| Title | test | last |"]
        target = ["Title | test | last"]

        result = geeknoteConvertorLib.convertToGeeknoteTable(source)

        self.assertEqual(result, target)

    def testConvertToGeeknoteTableHeader(self):
        source = ["|------+----+------|"]
        target = ["---|---|---"]

        result = geeknoteConvertorLib.convertToGeeknoteTable(source)

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTables(self):
        source = ["some text sdfsdf", "| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,26))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTablesNext(self):
        source = ["some text sdfsdf", "| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,26))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation(1,0))

        self.assertEqual(result, target)

    def testParseOrgTable(self):
        source = ["| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "| 2Content | 21 | 2Content Z |"]

        result = geeknoteConvertorLib.OrgParser.parse(source)

        self.assertEqual(result.getCols(0), 3)
        self.assertEqual(result.getRows(), 3)
        self.assertEqual(result.getColumnContent(0,0), "Header")
        self.assertEqual(result.getColumnContent(0,1), "Content")
        self.assertEqual(result.getColumnContent(0,2), "2Content")
        self.assertEqual(result.getColumnContent(1,0), "X")
        self.assertEqual(result.getColumnContent(1,1), "1")
        self.assertEqual(result.getColumnContent(1,2), "21")
        self.assertEqual(result.getColumnContent(2,0), "Header Z")
        self.assertEqual(result.getColumnContent(2,1), "Content Z")
        self.assertEqual(result.getColumnContent(2,2), "2Content Z")

        
