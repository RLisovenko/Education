import sys, math
#import numpy
# listList[StartPos:endPos:Step]
# myList[::-1] invertor List slaiz

def fCreate_Random_Array(mySizeArray = 3 ):
    """

    :return:
    """
    import numpy as np
    random.randint()
    np.random.seed(27)
    A = np.random.randint(1,10,size = (mySizeArray,3))
    B = np.random.randint(1,10,size = (mySizeArray,2))
    print(f"Matrix A:n {A}n")
    print(f"Matrix B:n {B}n")
    return A
    #---------------------------------
def fMultiply_Array(fArray_X: list, fArray_Y: list, fWelhesArrayOperation = "*") -> list:
    """
    одномерный массив {} чисел просто перемножить и сложить
    #-------------------------Array mit List
    return new array list
    """

    iLen_X = len(fArray_X)
    iLen_Y = len(fArray_Y)
    #print("Len iLen_X: ",iLen_X)
    #print("Len iLen_Y: ", iLen_Y)

    if iLen_X  == 0 or iLen_Y == 0:
          print("das array habe nicht varible! Len = ",iLen_X)
    elif iLen_X - iLen_Y == 0 or iLen_X - iLen_Y < 0 or iLen_X - iLen_Y > 0:
            iMyInd = 0
            fArray_Res = []
            while iMyInd < (iLen_X if iLen_X < iLen_Y else iLen_Y):
                    #fArray_Res.append(fArray_X[iMyInd] & fWelhesArrayOperation & fArray_Y[iMyInd])
                    fArray_Res.append(fArray_X[iMyInd] * fArray_Y[iMyInd])
                    #print("fArray_Res",fArray_Res)
                    iMyInd += 1
            return fArray_Res
    else:
        print("Different array len!",iLen_X - iLen_Y)
    return None

 #-----------------------------Begin Main porogramm
MyArray_1 = MyArray_2 = [1,2,3,4,5]
MyArray_2 = [1,2,3,4,6,7,8,9]
print("MyArray_Result->",fMultiply_Array(MyArray_1, MyArray_2, 3))
