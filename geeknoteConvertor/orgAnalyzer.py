import re
from utils import CacheLocation

"""
This file contains all classes for handling org mode specific objects
"""


class OrgTable:
    """
    This is an in meory representation of an org table
    """
    
    def __init__(self):
        """
        Create an empty OrgTable
        """
        self.__rows = []

    @classmethod
    def constructFromTable(cls, pTable):
        """
        Create an OrgTable object based on a matrix
        cls: The class (OrgTable), is suplied by the decorator
        pTable: A matrix, a list of lists, e.g. [["a", "b", "c"],[1, 2, 3]]
        """
        vOrgTable = cls()
        vOrgTable.__rows = pTable
        return vOrgTable
        
    def addHeader(self, pColIdx, pContent):
        vRow = self.__addRow(0)
        OrgTable.__addColumn(vRow, pColIdx)
        vRow[pColIdx] = pContent

    def addColumn(self, pColIdx, pRowIdx, pContent):
        vRow = self.__addRow(pRowIdx)
        OrgTable.__addColumn(vRow, pColIdx)
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

