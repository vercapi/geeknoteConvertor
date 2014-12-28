import re
from utils import cached, regexrepl, cacheFile
import enmlOutput
import orgOutput

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

def removeEmptyLines(pSource):
    while(len(pSource) > 0):
        vMatchEmptyLine = re.search("^[ ]*$", pSource[0])
        if vMatchEmptyLine != None:
            del pSource[0]
        else:
            break
        
    return pSource        

def org2ever(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache = enmlOutput.convertDoneToEvernote(pCache = vCache)
    vCache = enmlOutput.convertTodoToEvernote(pCache = vCache)
    vCache = enmlOutput.convertToEvernoteLinkNotation(pCache=vCache)
    vCache = escapeCharsFile(pSource=vCache, pChars=fEscapeChars)
    vCache =  enmlOutput.translateOrgToHTMLTables(pCache = vCache)
    writeFile(pDestinationFile, vCache)

def ever2org(pSourceFile, pDestinationFile):
    vCache = cacheFile(pSourceFile)
    vCache = removeEmptyLines(vCache)
    vCache = orgOutput.completeOrgTableNotation(vCache)
    vCache = unescapeCharsFile(vCache, fEscapeChars)
    vCache = orgOutput.convertToOrgLinkNotation(pSource=vCache)
    vCache = orgOutput.convertDoneToOrg(pCache = vCache)
    vCache = orgOutput.convertTodoToOrg(pCache = vCache)
    writeFile(pDestinationFile, vCache)
    

def writeFile(pDestinationFile, pCache):
    for line in pCache:
        if not line.endswith("\n"):
            line += "\n"
        pDestinationFile.write(line)
