#Fibinachi 100
#  0 1 1 2 3 5 8 13 21 33,,,
iBegin=0
iEnd=100
iNext=iVor=iCur=iCount=iBegin
iStep=iBegin+1
#  0 1 1 2 3 5 8 13 21 34 55,,,
for iCount in range(iBegin,iEnd,iStep):
    iNext = iCur + iVor
    if iCount == 0:
        print(iCount)
    elif  iCount==1:
        print(iCount)
        print(iCount)
        iVor = iCount
        iCur = iCount
    elif iCount==iNext:
        print(iCount)
        iVor = iCur
        iCur=iNext
    #else:
print("End von iteration For")

#------------------'
print("Begin iteration While")
iBegin=0
iEnd=100
iNext=iVor=iCur=iCount=iBegin
while True:
    iNext = iCur + iVor
    if iCount == 0:
        print(iCount)
    elif iCount == 1:
        print(iCount)
        print(iCount)
        iVor = iCount
        iCur = iCount
    elif iCount == iNext:
        print(iCount)
        iVor = iCur
        iCur = iNext
    elif iCount==iEnd:
        break
    iCount+=1
print("End von iteration - While")