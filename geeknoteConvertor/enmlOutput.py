import re
from utils import cached, regexrepl
from orgAnalyzer import OrgParser
from utils import CacheLocation

@cached
@regexrepl
def convertTodoToEvernote(pLine):
    return  re.subn(r'(^\**) TODO', r'\1<en-todo/>', pLine)
    

@cached
@regexrepl
def convertDoneToEvernote(pLine):
    return re.subn(r'(^\**) DONE', r'\1<en-todo checked="true"/>', pLine)

def translateOrgToHTMLTables(pCache):
    vNewCache = pCache
    vCacheRange = OrgParser.identifyOrgTable(vNewCache, CacheLocation.getZeroCacheLocation())
    while(vCacheRange.start != None and vCacheRange.start > CacheLocation.getZeroCacheLocation()):
        vOrgTablePart = CacheLocation.getCacheLocation(vNewCache, vCacheRange.start, vCacheRange.end)
        vOrgTable = OrgParser.parse(vOrgTablePart)
        vHTMLWriter = OrgTableHTMLWriter(vOrgTable)
        vCache = vHTMLWriter.parseHTML()
        vNewCache = CacheLocation.replaceCacheLocation(vNewCache, vCacheRange.start, vCacheRange.end, vCache)

        vOriginalLines = vCacheRange.end.getLineNum() - vCacheRange.start.getLineNum()
        vNewLines = len(vCache)
        vDifference = vNewLines - vOriginalLines        

        vCacheLocationEnd = CacheLocation(vCacheRange.end.getLineNum()+vDifference, vCacheRange.end.getIndex())
        vCacheRange = OrgParser.identifyOrgTable(vNewCache, vCacheLocationEnd)


    return vNewCache


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

class OrgTableHTMLWriter:

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
        self.__openTag(OrgTableHTMLWriter.TABLE_TAG)

    def __closeTable(self):
        self.__newLine()
        self.__closeTag(OrgTableHTMLWriter.TABLE_TAG)
        self.__newLine()

    def __addHeaderRow(self):
        self.__newLine()
        self.__openTag(OrgTableHTMLWriter.TR_TAG)

        vNumOfHeaders = self.__orgTable.getCols(0)
        for vColIdx in range(vNumOfHeaders):
            self.__addHeader(self.__orgTable.getColumnContent(vColIdx, 0))
            
        self.__closeTag(OrgTableHTMLWriter.TR_TAG)

    def __addRows(self):
        for vRowIdx in range(self.__orgTable.getRows()-1):
            self.__newLine()
            self.__addRow(vRowIdx+1)

    def __addRow(self, pRowNum):
        self.__openTag(OrgTableHTMLWriter.TR_TAG)

        for vColIdx in range(self.__orgTable.getCols(pRowNum)):
            self.__addCell(self.__orgTable.getColumnContent(vColIdx, pRowNum))
        
        self.__closeTag(OrgTableHTMLWriter.TR_TAG)

    def __addHeader(self, pContent):
        self.__addElement(OrgTableHTMLWriter.TH_TAG, pContent)

    def __addCell(self, pContent):
        self.__addElement(OrgTableHTMLWriter.TD_TAG, pContent)
        
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

