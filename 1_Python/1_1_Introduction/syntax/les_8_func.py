"""
Рекурсивні функціі
"""
def fFabinachi_Collection_Num(iNum_fib: int):
    # Fibinachi выводит числа фибоначи
    #  0 1 1 2 3 5 8 13 21 33,,,
    iBegin = 0
    iEnd = iNum_fib
    iNext = iVor = iCur = iCount = iBegin
    iStep = iBegin + 1

    #  правильніе чиса фибоначи 0 1 1 2 3 5 8 13 21 34 55,,,
    #  переделанные 1 2 3 5 8 13 21 34 55,,,
    for iCount in range(iBegin, iEnd+1, iStep):
        iNext = iCur + iVor
        #if iCount == 0:
            #-------print(iCount)

        if iCount == 1:
            print(iCount)
            print(iCount)
            iVor = iCount
            iCur = iCount
        elif iCount >= iNext and iCount != 0:
            print(iCount)
            iVor = iCur
            iCur = iNext
        # else:
    print("End von iteration For")

def fFabinachi_While(iNum: int) -> int:
    """
    выводит числ в ряду фибоначи по его порядковому  номеру
    :param iNum: номер in ряду
    :return: возращает само число
    """
    iFib1 = iFib2 = 1
    iCount=0
    while iCount < iNum - 2:
        fFib_sum = iFib1 + iFib2
        #-----ifib1 = iFib2
        #fFib2 = fFib_sum
        # тоже при помощи кортеджей также епе и предущая
        iFib1, iFib2 = iFib2, fFib_sum
        iCount += 1
        # iCount = iCount +1
    return iFib2
def fFibonachi_for(iNum):
    iFib1=iFib2=1
    for i in range(2,iNum):
        iFib1 , iFib2 = iFib2 ,iFib1 + iFib2
    return  iFib2
#----------------Fibonacjhi recursia
def fFib_Recursion(iNum):
    if iNum in (1, 2):
        print("In part")
        return 1
    else:
        print(f"step")
    #iFib_prev1 = fFib_Recursia(iNum-1)
    #iFib_prev2 = fFib_Recursia(iNum-2)
    return( fFib_Recursion(iNum-1)+fFib_Recursion(iNum-2) )

#--------------------
n_str=input("enter num von fibanache : ")
iNum=int(n_str)
#fFabinachi_Collection_Num(iNum)

#iNumFib=fFabinachi_While(iNum)
iNumFib =fFibonachi_for(iNum)
print(iNumFib)
#fFabinachi_Collection_Num(iNumFib)
fFib_Recursion(iNumFib)