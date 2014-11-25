import sys
import codecs
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
        target = ["[[www.google.be][Search]]"]
        source = ["[www.google.be](Search)"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInText(self):
        target = ["Here is some text and this is [[www.google.be][Search]] a link"]
        source = ["Here is some text and this is [www.google.be](Search) a link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationDoubleInText(self):
        target = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]
        source = ["Here is some [www.emacs.org](emacs) text and this is [www.google.be](Search) a link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToOrgLinkNotationInTextNoLink(self):
        target = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]
        source = ["Here is some text and this is [www.google.be](Search) a link", "no link"]

        result = geeknoteConvertorLib.convertToOrgLinkNotation(source)
        
        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotation(self):
        target = ["[Search](www.google.be)"]
        source = ["[[www.google.be][Search]]"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInText(self):
        target = ["Here is some text and this is [Search](www.google.be) a link"]
        source = ["Here is some text and this is [[www.google.be][Search]] a link"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationDoubleInText(self):
        target = ["Here is some [emacs](www.emacs.org) text and this is [Search](www.google.be) a link"]
        source = ["Here is some [[www.emacs.org][emacs]] text and this is [[www.google.be][Search]] a link"]

        result = geeknoteConvertorLib.convertToEvernoteLinkNotation(source)

        self.assertEqual(result, target)

    def testConvertToEvernoteLinkNotationInTextNoLink(self):
        target = ["Here is some text and this is [Search](www.google.be) a link", "no link"]
        source = ["Here is some text and this is [[www.google.be][Search]] a link", "no link"]

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
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,27))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTables2cols(self):
        source = ["some text sdfsdf", "| Header | X |", "|------+----|", "| Content | 1 |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,15))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTablesTrailingSpaces(self):
        source = ["some text sdfsdf", "| Header | X |  ", "|------+----|", "| Content | 1 |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,15))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTables3rows(self):
        source = ["some text sdfsdf", "| Header | X |", "|------+----|", "| Content | 1 |", "| Third | 2 |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(4,13))

        result = geeknoteConvertorLib.OrgParser.identifyOrgTable(source, geeknoteConvertorLib.CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTablesNext(self):
        source = ["some text sdfsdf", "| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "Some other text"]
        target = (geeknoteConvertorLib.CacheLocation(1,0), geeknoteConvertorLib.CacheLocation(3,27))

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

    def testParseOrgTable2Cols(self):
        source = ["| Header | X |", "|------+-----|", "| Content | 1 |", "| 2Content | 21 |"]

        result = geeknoteConvertorLib.OrgParser.parse(source)

        self.assertEqual(result.getCols(0), 2)
        self.assertEqual(result.getRows(), 3)
        self.assertEqual(result.getColumnContent(0,0), "Header")
        self.assertEqual(result.getColumnContent(0,1), "Content")
        self.assertEqual(result.getColumnContent(0,2), "2Content")
        self.assertEqual(result.getColumnContent(1,0), "X")
        self.assertEqual(result.getColumnContent(1,1), "1")
        self.assertEqual(result.getColumnContent(1,2), "21")
        
    def testOrgTableFromTabe(self):
        vTable = [["h"+str(i) for i in range(4)], ["c1"+str(i) for i in range(4)], ["c2"+str(i) for i in range(4)]]

        vOrgTable = geeknoteConvertorLib.OrgTable.constructFromTable(vTable)

        self.assertEqual(vOrgTable.getCols(0), 4)
        self.assertEqual(vOrgTable.getRows(), 3)
        self.assertEqual(vOrgTable.getColumnContent(0,0), "h0")
        self.assertEqual(vOrgTable.getColumnContent(1,0), "h1")
        self.assertEqual(vOrgTable.getColumnContent(2,0), "h2")
        self.assertEqual(vOrgTable.getColumnContent(0,1), "c10")
        self.assertEqual(vOrgTable.getColumnContent(1,1), "c11")
        self.assertEqual(vOrgTable.getColumnContent(2,1), "c12")
        self.assertEqual(vOrgTable.getColumnContent(0,2), "c20")
        self.assertEqual(vOrgTable.getColumnContent(1,2), "c21")
        self.assertEqual(vOrgTable.getColumnContent(2,2), "c22")

    def testWriteHtmlTable(self):
        vTable = [["h"+str(i) for i in range(4)], ["c1"+str(i) for i in range(4)], ["c2"+str(i) for i in range(4)]]

        vOrgTable = geeknoteConvertorLib.OrgTable.constructFromTable(vTable)
        vHTMLWriter = geeknoteConvertorLib.HTMLWriter(vOrgTable)
        vResult = vHTMLWriter.parseHTML()


        vTarget = ["<TABLE>"
                   ,"<TR><TH>h0</TH><TH>h1</TH><TH>h2</TH><TH>h3</TH></TR>"
                   ,"<TR><TD>c10</TD><TD>c11</TD><TD>c12</TD><TD>c13</TD></TR>"
                   ,"<TR><TD>c20</TD><TD>c21</TD><TD>c22</TD><TD>c23</TD></TR>"
                   ,"</TABLE>"]

        self.assertEqual(vResult, vTarget)

    def testGetCacheLocation(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = [" 1", "Word"]

        vCacheLocationStart = geeknoteConvertorLib.CacheLocation(1,4)
        vCacheLocationEnd = geeknoteConvertorLib.CacheLocation(2,4)
        vResult = geeknoteConvertorLib.getCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocation(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "My", "Text", "Last"]

        vReplacement = ["My", "Text"]

        vCacheLocationStart = geeknoteConvertorLib.CacheLocation(1,0)
        vCacheLocationEnd = geeknoteConvertorLib.CacheLocation(2,6)
        vResult = geeknoteConvertorLib.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocationWithin(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "Line My", "Text L", "Last"]

        vReplacement = ["My", "Text"]

        vCacheLocationStart = geeknoteConvertorLib.CacheLocation(1,5)
        vCacheLocationEnd = geeknoteConvertorLib.CacheLocation(2,4)
        vResult = geeknoteConvertorLib.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)

    def testReplaceCacheLocationDifirence(self):
        vSource = ["Test A", "Line 1", "Word L", "Last"]
        vTarget = ["Test A", "Line My", "Own", "Text L", "Last"]

        vReplacement = ["My", "Own", "Text"]

        vCacheLocationStart = geeknoteConvertorLib.CacheLocation(1,5)
        vCacheLocationEnd = geeknoteConvertorLib.CacheLocation(2,4)
        vResult = geeknoteConvertorLib.replaceCacheLocation(vSource, vCacheLocationStart, vCacheLocationEnd, vReplacement)

        self.assertEqual(vResult, vTarget)
    
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

        vCache = geeknoteConvertorLib.cacheFile(vSource)
        vResult = geeknoteConvertorLib.translateOrgToHTMLTables(vCache)
    
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

    def testConvertTodoToEvernote(self):
        source = ["*** TODO This is a task"]
        target = ["***<en-todo/> This is a task"]

        result = geeknoteConvertorLib.convertTodoToEvernote(source)

        self.assertEqual(target, result)

    def testConvertDoneToEvernote(self):
        source = ["*** DONE This is a task done"]
        target = ["***<en-todo checked=\"true\"/> This is a task done"]
        
        result = geeknoteConvertorLib.convertDoneToEvernote(source)

        self.assertEqual(target, result)

    def testConvertTodoToOrg(self):
        target = ["*** TODO This is a task"]
        source = ["***<en-todo/> This is a task"]

        result = geeknoteConvertorLib.convertTodoToOrg(source)

        self.assertEqual(target, result)

    def testConvertDoneToOrg(self):
        target = ["*** DONE This is a task done"]
        source = ["***<en-todo checked=\"true\"/> This is a task done"]

        result = geeknoteConvertorLib.convertDoneToOrg(source)

        self.assertEqual(target, result)    

    def testFullConversionToGeeknote(self):
        vSourceFile = codecs.open(filename="./resources/test.org", mode="r", encoding="utf-8")
        vDestinationFile = codecs.open(filename="./resources/test.out", mode="w+", encoding="utf-8")
        try:
            geeknoteConvertorLib.org2ever(vSourceFile, vDestinationFile)
        finally:
            vSourceFile.close()
            vDestinationFile.close()
