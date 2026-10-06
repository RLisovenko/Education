def fFunction_Test(a):
    a=3
    print(id(a))
    d='qwertz'
    print(len(d))
    s=any([False,False,False])
    print(s)
    a=print('a')
    print(a is None)
#---------------------------------------------
def fFunction_2(iBegin=0,iEnd=100,sStr="for",iStep=1):
    print(f'Arguments Function: ',{iBegin},{iEnd},{sStr})
    print("Begin von iteration ",sStr)

    iNext = iVor = iCur = iCount = iBegin
    if sStr=="While" or sStr=="while"  or sStr=="WHILE":
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
            elif iCount == iEnd:
                break
            iCount += 1
            #print("End von iteration - ",sStr)
    elif sStr =="for" or sStr =="For" or sStr =="FOR":
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
            #print("End von iteration - ",sStr)
    else:
        print("UnKnown argument-",sStr)
        #return fFunction_2
    print("End von iteration - ", sStr)

#-------------------------------------------Func 3
def fFunc_addStrToList(sAddStr=None):
    if sAddStr is None:
        sAddStr=[]
    else:
        sAddStr.append(sAddStr)
    return sAddStr
def fFunc_avg(iNum1=0,iNum2=1,iNum3=1):
        return (iNum1 + iNum2 + iNum3) / (bool(iNum1)+bool(iNum2)+bool(iNum3))
    #return (iNum1+iNum2+iNum3)/3

def fFunc_avg_universal(sList):
    fTotalSum=0
    for iCount in sList:
        fTotalSum+=iCount
    return fTotalSum/len(sList)
def fFunc_avg_universal_Cortage(*args):
    fTotalSum=0
    for iCount in args:
        fTotalSum+=iCount
    return fTotalSum/len(args)

def fFunc_Sum_universal_Cortage(**kwargs):
    print("kwargs",kwargs,print(type(kwargs)))
    for key,val in kwargs.items():
        print("key:",key,"--->val:",val)


#-----------------Call Function
#fFunction_2(iBegin=1,iEnd=333,sStr="for")
#print(a)
#fFunction_Test(True)
print(fFunc_addStrToList())
print(fFunc_addStrToList())
print(fFunc_addStrToList())
#print(fFunc_addStrToList([1,2,3]))
fFunc_addStrToList=None

print("Result fur fFunc_avg - ",fFunc_avg())
print("Result fur fFunc_avg_universal - ",fFunc_avg_universal([1,2,3,4,5,6,7,66]))
#---------------------------mit Cortage
print("Result fur fFunc_avg_universal_ via Cortage - ",fFunc_avg_universal_Cortage(1,2,3,4,5,6,7,77))
cCortage_Test=(1,2,3,4,5,6,7,77,88)
print("Result fur fFunc_avg_universal_ via Cortage - ",fFunc_avg_universal_Cortage(*cCortage_Test))
#-------------------------Cortage mit kvargs Slovar
fFunc_Sum_universal_Cortage(key1=1,key2=2,key3=3)
#------------Slovnik universal variabl
def fFunk_Uni_Diferent_Var(a,b,/,*args,**kwargs): #machen ne obyazatelnii parametr / nach enter
    print(f"a={a}")  # fix posiz elementu
    print(f"b={b}")
    print(f"args={args}")   # Any element group by Cortage
    print(f"kwargs={kwargs}")   #elementu type Slovar

fFunk_Uni_Diferent_Var("aaa",1,11,22,33,44,55,ss=666,vv=777)
#-----------------
fFunk_Uni_Diferent_Var("aaa",1)
#--------------------------Comment fur fanction

def fFuncCommentUndAnnot(a: int, b: int) -> int:
    #oder machen das rule def    fFuncComment(a,b,c):
     #-------------------func mit annotation def fFuncComment(a: int,b:str,c:List)->float:
    """DAs ist comment function
        Arguments description
        Annotation machen
        def fFuncComment(a: int,b:str,c:List)->float:
        fFuncComment.__doc__ ->das call comment
        fFuncComment.__annotation__ ->das call annotation von variable und was muss func return Type
    """
    return(3.141592653589793238462643)

# -------------pass # nicht machen

print(fFuncCommentUndAnnot.__doc__) #comment - documentation von function
print(fFuncCommentUndAnnot.__annotations__) #annotation documentation von function