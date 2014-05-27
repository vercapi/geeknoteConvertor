import re
from html.parser import HTMLParser
from subprocess import call

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

    def __findElementInCache(pCacheLocationStart, pSource, pElement):
        vSearchArea = pSource[pCacheLocationStart.getLineNum():]
        vSearchIndex = pCacheLocationStart.getIndex()
        vIndex = -1
        vLineNum = -1

        for index, line in enumerate(vSearchArea):
            vIndex = line.find(pElement, vSearchIndex)
            print("index: "+str(vIndex))
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
        
class OrgTable:
    
    def __init__(self):
        self.__rows = []

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


class CacheLocation(object):

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
fEscapeChars = ["_", "[", "]", "*"]

"""
Open a file with name pFileName
"""
def openFile(pFileName):
    vFile =  open(pFileName, "w")
    return vFile

"""
Escape all occurances of chars in pChars in pFile(file) 
backslash as it is defined in the markdown spec
"""
def processCharsFile(pSource, pChars, function):
    vCache = list()
    for line in pSource:
        vResult = function(pLine=line, pChars=pChars)
        vCache.append(vResult)

    return vCache

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

def replaceTables(pHTML):
    vCache = pHTML
    
    zero = CacheLocation.getZeroCacheLocation()
    vStartLocation = OrgHTMLParser.findTableStart(zero, pHTML)

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

def org2ever(pSourceFile, pDestinationFile):
    None
    # vCache = cacheFile(pSourceFile)
    # vCache =  escapeCharsFile(pSource=vCache, pChars=fEscapeChars)
    # writeFile(pDestinationFile, vCache)

def ever2org(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache = unescapeCharsFile(vCache, fEscapeChars)
    vCache = replaceTables(vCache)
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
