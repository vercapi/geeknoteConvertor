import re
from utils import cached, regexrepl

def completeOrgTableNotation(pSource):
    vCache = list()
    for vIdx, vLine in enumerate(pSource):
        vNewLine = vLine.rstrip()

        if vLine.find("|") >= 0:
            vLeadingPipe = re.search("^\|.*", vLine)
            if vLeadingPipe == None:
                vNewLine = "|"+vNewLine
            else:
                vNewLine = vNewLine
            
            vTrailingPipe = re.search(".*\|$", vLine)
            if vTrailingPipe == None:
                vNewLine = vNewLine+"|"

            vNewLine = vNewLine.replace("-|-", "-+-")
        else:
            vNextLine = ""
            if(len(pSource) > vIdx+1):
                vNextLine = pSource[vIdx+1]
            if len(vNewLine) == 0 and vNextLine.find("|") >= 0:
                vNewLine = None
            else:
                vNewLine = vLine    

        if vNewLine != None:
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
            vLink = vLinkResult.group(2)
            vLinkName = vLinkResult.group(1)

            vNewLink = "[["+vLink+"]["+vLinkName+"]]"
            vNewLine = vNewLine.replace(vLinkResult.group(0), vNewLink)
            
        vCache.append(vNewLine)
        vReplaced = True
        if not vReplaced:
            vCache.append(vLine)

    return vCache

@cached
@regexrepl
def convertTodoToOrg(pLine):
    return re.subn(r'(^\**)<en-todo/>', r'\1 TODO', pLine)

@cached
@regexrepl
def convertDoneToOrg(pLine):
    return re.subn(r'(^\**)<en-todo checked="true"/>', r'\1 DONE', pLine)
