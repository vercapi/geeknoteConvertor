import unittest

from orgAnalyzer import OrgTable
from orgAnalyzer import OrgParser
from utils import CacheLocation

class TestOrgAnalyzer(unittest.TestCase):
    None

    def testOrgParserIdentifyOrgTables(self):
        source = ["some text sdfsdf", "| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "Some other text"]
        target = (CacheLocation(1,0), CacheLocation(3,27))

        result = OrgParser.identifyOrgTable(source, CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTables2cols(self):
        source = ["some text sdfsdf", "| Header | X |", "|------+----|", "| Content | 1 |", "Some other text"]
        target = (CacheLocation(1,0), CacheLocation(3,15))

        result = OrgParser.identifyOrgTable(source, CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTablesTrailingSpaces(self):
        source = ["some text sdfsdf", "| Header | X |  ", "|------+----|", "| Content | 1 |", "Some other text"]
        target = (CacheLocation(1,0), CacheLocation(3,15))

        result = OrgParser.identifyOrgTable(source, CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTables3rows(self):
        source = ["some text sdfsdf", "| Header | X |", "|------+----|", "| Content | 1 |", "| Third | 2 |", "Some other text"]
        target = (CacheLocation(1,0), CacheLocation(4,13))

        result = OrgParser.identifyOrgTable(source, CacheLocation.getZeroCacheLocation())

        self.assertEqual(result, target)

    def testOrgParserIdentifyOrgTablesNext(self):
        source = ["some text sdfsdf", "| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "Some other text"]
        target = (CacheLocation(1,0), CacheLocation(3,27))

        result = OrgParser.identifyOrgTable(source, CacheLocation(1,0))

        self.assertEqual(result, target)

    def testParseOrgTable(self):
        source = ["| Header | X | Header Z |", "|------+----+------|", "| Content | 1 | Content Z |", "| 2Content | 21 | 2Content Z |"]

        result = OrgParser.parse(source)

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

        result = OrgParser.parse(source)

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

        vOrgTable = OrgTable.constructFromTable(vTable)

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

