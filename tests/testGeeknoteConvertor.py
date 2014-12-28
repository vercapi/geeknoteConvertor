import sys
import codecs
sys.path.append("../geeknoteConvertor")

import geeknoteConvertorLib
import unittest
from orgAnalyzer import OrgTable
from enmlOutput import OrgTableHTMLWriter
import utils

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

    def testWriteHtmlTable(self):
        vTable = [["h"+str(i) for i in range(4)], ["c1"+str(i) for i in range(4)], ["c2"+str(i) for i in range(4)]]

        vOrgTable = OrgTable.constructFromTable(vTable)
        vHTMLWriter = OrgTableHTMLWriter(vOrgTable)
        vResult = vHTMLWriter.parseHTML()


        vTarget = ["<TABLE>"
                   ,"<TR><TH>h0</TH><TH>h1</TH><TH>h2</TH><TH>h3</TH></TR>"
                   ,"<TR><TD>c10</TD><TD>c11</TD><TD>c12</TD><TD>c13</TD></TR>"
                   ,"<TR><TD>c20</TD><TD>c21</TD><TD>c22</TD><TD>c23</TD></TR>"
                   ,"</TABLE>"]

        self.assertEqual(vResult, vTarget)


    def testFullConversionToGeeknote(self):
        vSourceFile = codecs.open(filename="./resources/test.org", mode="r", encoding="utf-8")
        vDestinationFile = codecs.open(filename="./resources/test.evernote.out", mode="w+", encoding="utf-8")
        try:
            geeknoteConvertorLib.org2ever(vSourceFile, vDestinationFile)
        finally:
            vSourceFile.close()
            vDestinationFile.close()

        vResultFile = codecs.open(filename="./resources/test.evernote.out", mode="r", encoding="utf-8")
        vTargetFile = codecs.open(filename="./resources/test.evernote.target", mode="r", encoding="utf-8")
        
        try:
            vResult = utils.cacheFile(vResultFile)
            vTarget = utils.cacheFile(vTargetFile)
            self.assertEqual(vResult, vTarget)
        except Exception as e:
            self.assertTrue(False, "Exception happened while comparing files: "+str(e))
        finally:
            vResultFile.close()
            vTargetFile.close()
            
    def testFullConversionToOrgMode(self):
        vSourceFile = codecs.open(filename="./resources/test.evernote", mode="r", encoding="utf-8")
        vDestinationFile = codecs.open(filename="./resources/test.org.out", mode="w+", encoding="utf-8")
        try:
            geeknoteConvertorLib.ever2org(vSourceFile, vDestinationFile)
        finally:
            vSourceFile.close()
            vDestinationFile.close()

        vResultFile = codecs.open(filename="./resources/test.org.out", mode="r", encoding="utf-8")
        vTargetFile = codecs.open(filename="./resources/test.org.target", mode="r", encoding="utf-8")
        
        try:
            vResult = utils.cacheFile(vResultFile)
            vTarget = utils.cacheFile(vTargetFile)
            self.assertEqual(vResult, vTarget)
        except Exception as e:
            self.assertTrue(False, "Exception happened while comparing files: "+str(e))
        finally:
            vResultFile.close()
            vTargetFile.close()
