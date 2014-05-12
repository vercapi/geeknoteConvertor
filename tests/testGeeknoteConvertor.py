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

# <table border="2" cellspacing="0" cellpadding="6" rules="groups" frame="hsides">


# <colgroup>
# <col  class="right" />

# <col  class="left" />

# <col  class="left" />
# </colgroup>
# <thead>
# <tr>
# <th scope="col" class="right">id</th>
# <th scope="col" class="left">name</th>
# <th scope="col" class="left">description</th>
# </tr>
# </thead>

# <tbody>
# <tr>
# <td class="right">1</td>
# <td class="left">Page one</td>
# <td class="left">This is some longer text</td>
# </tr>


# <tr>
# <td class="right">2</td>
# <td class="left">Other thing</td>
# <td class="left">This is awesome</td>
# </tr>
# </tbody>
# </table>
