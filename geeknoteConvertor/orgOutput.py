import re
from utils import cached, regexrepl

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
@regexrepl
def convertTodoToOrg(pLine):
    return re.subn(r'(^\**)<en-todo/>', r'\1 TODO', pLine)

@cached
@regexrepl
def convertDoneToOrg(pLine):
    return re.subn(r'(^\**)<en-todo checked="true"/>', r'\1 DONE', pLine)
