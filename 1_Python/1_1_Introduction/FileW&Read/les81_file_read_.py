"""
arbeite mit file

read()
write()
objFile.close()

import sys.stdin ввод
import sys.stdout поток вывода
import stderr - поток ошибок
import array

"""
import io
import os
#------------------------------

try:
    #bjFile = open(file="data/file.txt",mode="r", buffering=9, encoding="UTF-8" )
    #oder
    myUniversalFileName = os.path.join('data','file.txt' )
    objFile = open(myUniversalFileName)
    print("objFile.read -------------------\n",objFile.read())
except IOError:
    pass
finally: #в любом случае закріть
    objFile.close()
