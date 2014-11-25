import re
from html.parser import HTMLParser
from collections import namedtuple

def cached(function):
    def func_wrapper(pCache, *args):
        vCache = list()
        for vLine in pCache:
            vCache.append(function(vLine, *args))

        return vCache
    return func_wrapper

def regexrepl(function):
    def func_wrapper(pLine):
        vResult = function(pLine)
        if vResult[1] > 0:
            return vResult[0]
        else:
            return pLine
        
    return func_wrapper

class HTMLToENML:

    def removeHtmlAttribute(pSource, pAttribute):
        vCache = list()
        for line in pSource:
            vReplacement = re.sub(pAttribute+'=[\'\"][^\'^\"]*[\'\"]', '', line)
            vCache.append(vReplacement)

        return vCache

class OrgHTMLParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=False)
        
        self.__currentTag = None
        self.__currentRow = 0
        self.__currentCol = 0

    def handle_starttag(self, tag, attrs):
        self.__currentTag = tag

        if tag == "table":
            self.__currentTable = OrgTable()
        
    def handle_endtag(self, tag):
        self.__currentTag = None

        if tag == "tr":
            self.__currentRow += 1
            self.__currentCol = 0

        if tag in ("th", "td"):
            self.__currentCol += 1

    def handle_data(self, data):
        if self.__currentTag == "td":
            self.__currentTable.addColumn(pColIdx = self.__currentCol, pRowIdx = self.__currentRow, pContent = data)

        if self.__currentTag == "th":
            self.__currentTable.addHeader(pColIdx = self.__currentCol,  pContent = data)

    def getTable(self):
        return self.__currentTable

    def findTableStart(pCacheLocationStart, pSource):
        return OrgHTMLParser.__findElementInCache(pCacheLocationStart, pSource, "<table")

    def findTableEnd(pCacheLocationStart, pSource):
        vOriginalCacheLocation = OrgHTMLParser.__findElementInCache(pCacheLocationStart, pSource, "</table>")
        vCacheLocation = CacheLocation(vOriginalCacheLocation.getLineNum(), vOriginalCacheLocation.getIndex()+7)
        return vCacheLocation

    def findFirstDiv(pSource):
        vCacheLocation = CacheLocation(0,0)
        return OrgHTMLParser.__findElementInCache(vCacheLocation, pSource, "<div")

    def findLastDiv(pSource):
        vResultCacheLocation = CacheLocation.getNotFoundCacheLocation()
        vCacheLocation = CacheLocation(0,0)
        vCacheLocation = OrgHTMLParser.__findElementInCache(vCacheLocation, pSource, "</div>")
        while vCacheLocation != CacheLocation.getNotFoundCacheLocation():
            vCacheLocation = CacheLocation(vCacheLocation.getLineNum(), vCacheLocation.getIndex()+5)
            vResultCacheLocation = vCacheLocation
            vCacheLocation = OrgHTMLParser.__findElementInCache(vCacheLocation, pSource, "</div>")

        return vResultCacheLocation

    def __findElementInCache(pCacheLocationStart, pSource, pElement):
        vSearchArea = pSource[pCacheLocationStart.getLineNum():]
        vSearchIndex = pCacheLocationStart.getIndex()
        vIndex = -1
        vLineNum = -1

        for index, line in enumerate(vSearchArea):
            vIndex = line.find(pElement, vSearchIndex)
            vSearchIndex = 0
            if vIndex >= 0:                
                vLineNum = index
                break

        if vIndex >=0:
            vLineNum += pCacheLocationStart.getLineNum()
        else:
            vLineNum = -1

        vCacheLocation = CacheLocation(vLineNum, vIndex)
        return vCacheLocation

class OrgParser:

    def identifyOrgTable(pSource, pCacheLocationStart):
        vStartIdx = pCacheLocationStart.getLineNum()
        vSearchArea = pSource[pCacheLocationStart.getLineNum():]
        
        vStart = None
        vEnd = None
        vLineIdx = 0
        for vLine in vSearchArea:
            vLine = vLine.strip()
            vTableStart = re.search("^\|.*\|$", vLine)
            if vTableStart != None:
                vStart = CacheLocation(vLineIdx+vStartIdx, vTableStart.start())
                break
            
            vLineIdx += 1

        for vLine in vSearchArea[vLineIdx+1:]:
            vLine = vLine.strip()
            vTableEnd = re.search("^\|.*\|$", vLine)
            if vTableEnd == None:
                vEnd = CacheLocation(vLineIdx+vStartIdx, re.search("\|$", vSearchArea[vLineIdx].strip()).start()+1)
                break
            
            vLineIdx += 1

            
        return CacheLocation.CacheRange(vStart, vEnd)

    def parse(pTableCache):
        vOrgTtable = OrgTable()
        OrgParser.__parseHeader(pTableCache[0], vOrgTtable)
        for vIdx, vItem in enumerate(pTableCache[2:]):
            OrgParser.__parseColumns(vItem, vIdx+1, vOrgTtable)

        return vOrgTtable

    def __prepareLine(pLine):
         vCols = [item.strip() for item in pLine.split("|")]
         vCols = vCols[1:-1]

         return vCols

    def __parseHeader(pLine, pOrgTable):
        vCols = OrgParser.__prepareLine(pLine)

        for vIdx, vItem in enumerate(vCols):
            pOrgTable.addHeader(vIdx, vItem)

    def __parseColumns(pLine, pRowIdx, pOrgTable):
        vCols = OrgParser.__prepareLine(pLine)
        
        for vIdx, vItem in enumerate(vCols):
            pOrgTable.addColumn(vIdx, pRowIdx, vItem)
            
class OrgTable:
    
    def __init__(self):
        self.__rows = []

    @classmethod
    def constructFromTable(cls, pTable):
        vOrgTable = cls()
        vOrgTable.__rows = pTable
        return vOrgTable
        
    def addHeader(self, pColIdx, pContent):
        vRow = self.__addRow(0)
        vCol = OrgTable.__addColumn(vRow, pColIdx)
        vRow[pColIdx] = pContent

    def addColumn(self, pColIdx, pRowIdx, pContent):
        vRow = self.__addRow(pRowIdx)
        vCol = OrgTable.__addColumn(vRow, pColIdx)
        vRow[pColIdx] = pContent

    def getColumnSize(self, pColIdx):
        vMax = 0
        for row in self.__rows:
            vColSize = len(row[pColIdx])
            if vColSize > vMax:
                vMax = vColSize
                
        return vMax

    def getColumnContent(self, pColIdx, pRowIdx):
        return self.__rows[pRowIdx][pColIdx]

    def getRows(self):
        return len(self.__rows)

    def getCols(self, pRowIdx):
        return len(self.__rows[pRowIdx])

    def getTable(self):
        return self.__rows

    def __addRow(self, pRowIdx):
        if len(self.__rows)-1 < pRowIdx:
           self.__rows.append([])

        return self.__rows[pRowIdx]

    def __addColumn(pRow, pColIdx):
        if len(pRow)-1 < pColIdx:
           pRow.append("")

        return pRow[pColIdx]
        
        
class OrgWriter:

    def __init__(self, pOrgTable):
        self.__orgTable = pOrgTable
        self.__rows = pOrgTable.getRows()
        self.__cols = pOrgTable.getCols(0)

        self.__string = ""

    def generate(self):
        vContent = self.printSeparatorLine()
        vContent += self.printRow(0)
        vContent += self.printSeparatorLine()
        for i in range(self.__rows-1):
            vContent += self.printRow(i+1)

        vContent += self.printSeparatorLine()

        return vContent

    def printSeparatorLine(self):
        vContent = "|"
        for i in range(self.__cols):
            vSize = self.__orgTable.getColumnSize(i)
            vContent += "-"*(vSize+2) + "+"
        
        vContent = vContent[:-1]+"|\n"
        
        return vContent

    def printRow(self, pRowIdx):
        vContent = "|"
        for i in range(self.__cols):
            vContent += self.printColumn(pRowIdx, i)
        vContent += "\n"
        
        return vContent
            
    def printColumn(self, pRowIdx, pColIdx):
        vSize = self.__orgTable.getColumnSize(pColIdx)
        vContent = self.__orgTable.getColumnContent(pColIdx, pRowIdx)
        return " "+vContent.ljust(vSize+1)+"|"

class HTMLWriter:

    TABLE_TAG = "TABLE"
    TR_TAG = "TR"
    TH_TAG = "TH"
    TD_TAG = "TD"

    def __init__(self, pOrgTable):
        self.__orgTable = pOrgTable
        self.__cache = list()
        self.__currentLine = None

    def parseHTML(self):
        self.__openTable()
        self.__addHeaderRow()
        if(self.__orgTable.getRows() > 0):
            self.__addRows()
        self.__closeTable()
        
        return self.__cache

    def __openTable(self):
        self.__newLine()
        self.__openTag(HTMLWriter.TABLE_TAG)

    def __closeTable(self):
        self.__newLine()
        self.__closeTag(HTMLWriter.TABLE_TAG)
        self.__newLine()

    def __addHeaderRow(self):
        self.__newLine()
        self.__openTag(HTMLWriter.TR_TAG)

        vNumOfHeaders = self.__orgTable.getCols(0)
        for vColIdx in range(vNumOfHeaders):
            self.__addHeader(self.__orgTable.getColumnContent(vColIdx, 0))
            
        self.__closeTag(HTMLWriter.TR_TAG)

    def __addRows(self):
        for vRowIdx in range(self.__orgTable.getRows()-1):
            self.__newLine()
            self.__addRow(vRowIdx+1)

    def __addRow(self, pRowNum):
        self.__openTag(HTMLWriter.TR_TAG)

        for vColIdx in range(self.__orgTable.getCols(pRowNum)):
            self.__addCell(self.__orgTable.getColumnContent(vColIdx, pRowNum))
        
        self.__closeTag(HTMLWriter.TR_TAG)

    def __addHeader(self, pContent):
        self.__addElement(HTMLWriter.TH_TAG, pContent)

    def __addCell(self, pContent):
        self.__addElement(HTMLWriter.TD_TAG, pContent)
        
    def __addElement(self, pTagName, pContent):
        self.__openTag(pTagName)
        self.__currentLine += pContent
        self.__closeTag(pTagName)
    
    def __openTag(self, pTagName):
        self.__currentLine += "<"+pTagName+">"

    def __closeTag(self, pTagName):
        self.__currentLine += "</"+pTagName+">"

    def __newLine(self):
        if self.__currentLine and len(self.__currentLine.strip()) > 0:
            self.__cache.append(self.__currentLine)

        self.__currentLine = "";
    
class CacheLocation(object):

    CacheRange = namedtuple('CacheRange', 'start end')
    
    def __init__(self, pLineNum, pIndex):
        self.__lineNum = pLineNum
        self.__index = pIndex

    def getIndex(self):
        return self.__index

    def getLineNum(self):
        return self.__lineNum

    def getZeroCacheLocation():
        return CacheLocation(0,0)

    def getNotFoundCacheLocation():
        return CacheLocation(-1, -1)

    def __eq__(self, other):
        vEquals = False
        if isinstance(other, self.__class__):
            vEquals = other.getLineNum() == self.__lineNum and other.getIndex() == self.__index

        return vEquals

    def __lt__(self, other):
        return -1 == self.__compare(other)

    def __gt__(self, other):
        return 1 == self.__compare(other)

    def __ge__(self, other):
        return self.__compare(other) in (1,0)

    def __le__(self, other):
        return self.__compare(other) in (-1,0)

    def __compare(self, other):
        vCmp = 0
        
        if(self.__lineNum == other.getLineNum()):
            if(self.__index == other.getIndex()):
                vCmp = 0
            elif(self.__index > other.getIndex()):
                vCmp = 1
            else:
                vCmp = -1
        else:
            if(self.__lineNum > other.getLineNum()):
                vCmp = 1
            else:
                vCmp = -1

        return vCmp

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return str(self.__class__)+" -> "+"index: "+str(self.__index)+", lineNum:"+str(self.__lineNum)

# Characters to escape
fEscapeChars = ["_", "*"]

"""
Open a file with name pFileName
"""
def openFile(pFileName):
    vFile =  open(pFileName, "w")
    return vFile

@cached
def processCharsFile(pLine, pChars, function):
    return function(pLine=pLine, pChars=pChars)

def escapeCharsFile(pSource, pChars):
    return processCharsFile(pSource, pChars, escapeChars)

def unescapeCharsFile(pSource, pChars):
    return processCharsFile(pSource, pChars, unescapeChars)

def replaceCharFile(pSource, pChar, pSubstitute):
    vCache = list()
    for line in pSource:
        vResult = replaceChar(pLine=line, pChar=pChar, pSubstitute=pSubstitute)
        vCache.append(vResult)

    return vCache

def escapeChars(pLine, pChars):
    vLine = pLine
    for char in pChars:
        vLine = replaceChar(pLine=vLine, pChar=char, pSubstitute="\\"+char)
    
    return vLine

def unescapeChars(pLine, pChars):
    vLine = pLine
    for char in pChars:
        vLine = replaceChar(pLine=vLine, pChar="\\"+char, pSubstitute=char)
    
    return vLine

def replaceChar(pLine, pChar, pSubstitute):
    vResult = re.sub(re.escape(pChar), pSubstitute, pLine)
    return vResult

def replaceTables(pSource):
    vCache = pSource
    
    zero = CacheLocation.getZeroCacheLocation()
    vStartLocation = OrgHTMLParser.findTableStart(zero, pSource)

    while vStartLocation != CacheLocation.getNotFoundCacheLocation():
        vEndLocation = OrgHTMLParser.findTableEnd(vStartLocation, vCache)
        if vEndLocation > zero:
            vNewCache = vCache[:vStartLocation.getLineNum()]
            vLine = [vCache[vStartLocation.getLineNum()][:vStartLocation.getIndex()]]
            if len(vLine[0]) > 0:
                vNewCache += vLine
            
            vReplacement = [vCache[vStartLocation.getLineNum()][vStartLocation.getIndex():]]
            vReplacement += vCache[vStartLocation.getLineNum()+1:vEndLocation.getLineNum()]
            if vEndLocation.getLineNum() > vStartLocation.getLineNum():
                vReplacement += [vCache[vEndLocation.getLineNum()][:vEndLocation.getIndex()]]

            vParser = OrgHTMLParser()
            vParser.feed(''.join(vReplacement))
            vOrgTable = vParser.getTable()
            vOrgWriter = OrgWriter(vOrgTable)
            vNewCache += vOrgWriter.generate().splitlines()

            vLine = [vCache[vEndLocation.getLineNum()][vEndLocation.getIndex()+1:]]
            if len(vLine[0]) > 0:
                vNewCache += vLine
            vNewCache += vCache[vEndLocation.getLineNum()+1:]
            vCache = vNewCache
        vStartLocation = OrgHTMLParser.findTableStart(vEndLocation, vNewCache)

    return vCache

def removeHeader(pSource):
    vCacheLocationStart = OrgHTMLParser.findFirstDiv(pSource)
    vCacheLocationEnd = OrgHTMLParser.findLastDiv(pSource)

    vStart = vCacheLocationStart.getLineNum()
    vEnd = vCacheLocationEnd.getLineNum()
    
    #Assuming this block uses full lines and there is only 1 div
    vCache = pSource[vEnd+1:]
    return vCache

def removeEmptyLines(pSource):
    while(len(pSource) > 0):
        vMatchEmptyLine = re.search("^[ ]*$", pSource[0])
        if vMatchEmptyLine != None:
            del pSource[0]
        else:
            break
        
    return pSource    

def completeOrgTableNotation(pSource):
    vCache = list()
    for vLine in pSource:
        vNewLine = ""

        if vLine.find("|") >= 0:
            vLeadingPipe = re.search("^\|.*", vLine)
            if vLeadingPipe == None:
                vNewLine = "|"+vLine
            else:
                vNewLine = vLine
            
            vTrailingPipe = re.search(".*\|$", vLine)
            if vTrailingPipe == None:
                vNewLine = vNewLine+"|"

            vNewLine = vNewLine.replace("-|-", "-+-")
        else:
            vNewLine = vLine    
                
        vCache.append(vNewLine)

    return vCache

def convertToOrgLinkNotation(pSource):
    vCache = list()
    for vLine in pSource:
        vNewLine = ""
        vReplaced = False

        vNewLine = vLine
        while True:
            vLinkResult = re.search("\[([^\]]*)\]\(([^\)]*)\)", vNewLine)
            if not vLinkResult:
                break
            vLink = vLinkResult.group(1)
            vLinkName = vLinkResult.group(2)

            vNewLink = "[["+vLink+"]["+vLinkName+"]]"
            vNewLine = vNewLine.replace(vLinkResult.group(0), vNewLink)
            
        vCache.append(vNewLine)
        vReplaced = True
        if not vReplaced:
            vCache.append(vLine)

    return vCache

@cached
def convertToEvernoteLinkNotation(pLine):
        vNewLine = pLine
        while True:
            vLinkResult = re.search('\[\[([^\]]*)\]\[(([^\]]*))\]\]', vNewLine)
            if vLinkResult == None:
                break
            vLink = vLinkResult.group(1)
            vLinkName = vLinkResult.group(2)

            vNewLink = "["+vLinkName+"]("+vLink+")"
            vNewLine = vNewLine.replace(vLinkResult.group(0), vNewLink)
            vNewLine = vNewLine.replace('\\', '')

        return vNewLine
        

def convertToGeeknoteTable(pSource):
    vCache = list()
    for vLine in pSource:

        vNewLine = re.sub('^\|', '', vLine)
        vNewLine = re.sub('\|$', '', vNewLine)

        vHeaderResult =  re.search("(-*\+-*)+", vNewLine)
        if vHeaderResult != None:
            vNewLine = vNewLine.replace("+", "|")
            vNewLine = re.sub(r'\-*(\|*)', r'---\1', vNewLine)
        
        vCache.append(vNewLine.strip())

    return vCache


def getCacheLocation(pCache, pCacheLocationStart, pCacheLocationEnd):
    vFirstLine = pCacheLocationStart.getLineNum()
    vLastLine = pCacheLocationEnd.getLineNum()

    vIndexFirstLine = pCacheLocationStart.getIndex()
    vIndexLastLine = pCacheLocationEnd.getIndex()
    
    vLines = pCache[vFirstLine:vLastLine+1]
    vLines[0] = vLines[0][vIndexFirstLine:]
    vLines[-1] = vLines[-1][:vIndexLastLine]

    return vLines

def replaceCacheLocation(pCache, pCacheLocationStart, pCacheLocationEnd, pReplacement):
    vFirstLine = pCacheLocationStart.getLineNum()
    vLastLine = pCacheLocationEnd.getLineNum()

    vIndexFirstLine = pCacheLocationStart.getIndex()
    vIndexLastLine = pCacheLocationEnd.getIndex()

    vCache = pCache
    vCache[vFirstLine] = vCache[vFirstLine][:vIndexFirstLine] + pReplacement[0]
    vCache[vLastLine] = pReplacement[-1] + vCache[vLastLine][vIndexLastLine:]

    vCacheTmp = vCache[:vFirstLine+1]
    vCacheTmp += vCache[vLastLine:]
    vCache = vCacheTmp

    vRestReplacement = pReplacement[1:-1]
    for vLineIdx in range(len(vRestReplacement)):
        vCache.insert(vFirstLine+vLineIdx+1, vRestReplacement[vLineIdx])

    return vCache


def translateOrgToHTMLTables(pCache):
    vNewCache = pCache
    vCacheRange = OrgParser.identifyOrgTable(vNewCache, CacheLocation.getZeroCacheLocation())
    while(vCacheRange.start != None and vCacheRange.start > CacheLocation.getZeroCacheLocation()):
        vOrgTablePart = getCacheLocation(vNewCache, vCacheRange.start, vCacheRange.end)
        vOrgTable = OrgParser.parse(vOrgTablePart)
        vHTMLWriter = HTMLWriter(vOrgTable)
        vCache = vHTMLWriter.parseHTML()
        vNewCache = replaceCacheLocation(vNewCache, vCacheRange.start, vCacheRange.end, vCache)

        vOriginalLines = vCacheRange.end.getLineNum() - vCacheRange.start.getLineNum()
        vNewLines = len(vCache)
        vDifference = vNewLines - vOriginalLines        

        vCacheLocationEnd = CacheLocation(vCacheRange.end.getLineNum()+vDifference, vCacheRange.end.getIndex())
        vCacheRange = OrgParser.identifyOrgTable(vNewCache, vCacheLocationEnd)


    return vNewCache

@cached
@regexrepl
def convertTodoToEvernote(pLine):
    return  re.subn(r'(^\**) TODO', r'\1<en-todo/>', pLine)
    

@cached
@regexrepl
def convertDoneToEvernote(pLine):
    return re.subn(r'(^\**) DONE', r'\1<en-todo checked="true"/>', pLine)

@cached
@regexrepl
def convertTodoToOrg(pLine):
    return re.subn(r'(^\**)<en-todo/>', r'\1 TODO', pLine)

@cached
@regexrepl
def convertDoneToOrg(pLine):
    return re.subn(r'(^\**)<en-todo checked="true"/>', r'\1 DONE', pLine)
    

def org2ever(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache = convertDoneToEvernote(pCache = vCache)
    vCache = convertTodoToEvernote(pCache = vCache)
    #vCache = removeHeader(vCache)
    #vCache = replaceCharFile(vCache, "****.", "1")
    vCache = convertToEvernoteLinkNotation(pCache=vCache)
    vCache = escapeCharsFile(pSource=vCache, pChars=fEscapeChars)
    # vCache = HTMLToENML.removeHtmlAttribute(pSource=vCache, pAttribute='frame')
    # vCache = HTMLToENML.removeHtmlAttribute(pSource=vCache, pAttribute='rules')
    # vCache = HTMLToENML.removeHtmlAttribute(pSource=vCache, pAttribute='scope')
    # vCache = HTMLToENML.removeHtmlAttribute(pSource=vCache, pAttribute='class')
    # vCache = HTMLToENML.removeHtmlAttribute(pSource=vCache, pAttribute='id')
    vCache =  translateOrgToHTMLTables(pCache = vCache)
#    vCache = escapeChars(vCache, "*", "\\*")
    #vCache = convertToGeeknoteTable(pSource=vCache)
    writeFile(pDestinationFile, vCache)

def ever2org(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache = removeEmptyLines(vCache)
#    vCache = removeHeader(vCache)
#    vCache = replaceTables(vCache)
    vCache = completeOrgTableNotation(vCache)
    vCache = unescapeCharsFile(vCache, fEscapeChars)
 #   vCache = replaceCharFile(vCache, "#", "*")
 #   vCache = replaceCharFile(vCache, "1.", "****")
    vCache = convertToOrgLinkNotation(pSource=vCache)
    vCache = convertDoneToOrg(pCache = vCache)
    vCache = convertTodoToOrg(pCache = vCache)
    writeFile(pDestinationFile, vCache)
    
def cacheFile(pSourceFile):
    vCache = list()
    for line in pSourceFile:
        vCache.append(line)

    return vCache

def writeFile(pDestinationFile, pCache):
    for line in pCache:
        if not line.endswith("\n"):
            line += "\n"
        pDestinationFile.write(line)
