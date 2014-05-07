import re

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

def org2ever(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache =  escapeCharsFile(pSource=vCache, pChars=fEscapeChars)
    writeFile(pDestinationFile, vCache)

def ever2org(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache =unescapeCharsFile(vCache, fEscapeChars)
    writeFile(pDestinationFile, vCache)

def cacheFile(pSourceFile):
    vCache = list()
    for line in pSourceFile:
        vCache.append(line)

    return vCache

def writeFile(pDestinationFile, pCache):
    for line in pCache:
        pDestinationFile.write(line)
