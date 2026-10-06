#--------List []
#--------dDict_1={'key1':'ein','key2':2}
#--------sStr='qwerty'

#----------------------------------------------------
sList_All=["as","bar","qwerty"] #--------List
sList_En="qwerty"
sList_De="qwertz"
iCountIndex=0
iLenList_All=len(sList_All)

while iCountIndex < iLenList_All:
    if sList_All[iCountIndex]==sList_De:
        print("De keyboard layot")
        break
    elif sList_All[iCountIndex]==sList_En:
        print("En keyboard layot")
        break
    else:
        print("Andere keyboard layot",sList_All[iCountIndex])
    #    break
    iCountIndex += 1
else:
    print("Not findet layot")

