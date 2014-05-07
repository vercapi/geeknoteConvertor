import os
import sys
import geeknoteConvertorLib


if len(sys.argv) >= 2:
    vOriginal = sys.argv[1]
    vTmp = sys.argv[1]+".org"

    vSourceFile = open(vOriginal, "r")
    vDestinationFile = open(vTmp, "w+")
    try:
        geeknoteConvertorLib.ever2org(vSourceFile, vDestinationFile)
    finally:
        vSourceFile.close()
        vDestinationFile.close()
    
    os.system("emacsclient "+vTmp)

    vSourceFile = open(vTmp, "r")
    vDestinationFile = open(vOriginal, "w+")
    try:
        geeknoteConvertorLib.org2ever(vSourceFile, vDestinationFile)
    finally:
        vSourceFile.close()
        vDestinationFile.close()
        os.remove(vTmp)
    

    
