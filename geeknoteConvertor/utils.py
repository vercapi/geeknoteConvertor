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

def cacheFile(pSourceFile):
    vCache = list()
    for line in pSourceFile:
        vCache.append(line)

    return vCache

class CacheLocation(object):

    CacheRange = namedtuple('CacheRange', 'start end')
    
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
