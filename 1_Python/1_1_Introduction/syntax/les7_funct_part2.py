"""
Function internal und External
"""
def fExternal():
    def fInternal():
        iNum=123
        sStr=str(iNum)
        print(f"Type of iNum: {type(iNum)}=>",iNum)
        print(f"Type of sStr: {type(sStr)}=>",sStr)
        return 1
    print(fInternal())
    def fInternal_List():
        sStr="qwertz"
        myList=list(sStr)
        print(f"Type of sStr: {type(sStr)}=>", sStr)
        print(f"Type of myList: {type(myList)}=>", myList)

    print(fInternal_List())

    def fInternal_List():
        sStr="qwertz"
        myList=list(sStr)
        #--------Set okject to iterable
        sStr_2=iter(sStr)
        iStep_1=next(sStr_2)
        print("iStep_1=",iStep_1)
        iStep_2=next(sStr_2)
        print(iStep_2)
        print(f"Type of sStr: {type(sStr)}=>", sStr)
        print(f"Type of myList: {type(myList)}=>", myList)
    print(fInternal_List())
    def fInternal_List_bool():
        sStr="qwertz"
        myList_1=list(sStr)
        myList_2=[None] # Das List habe ein var
        myList_3=[] #Das ist Empty List
        print(f"my_List_3 when ist Empty: {bool(myList_3)}")
        print(f"my_List_2 when ist None: {bool(myList_2)}")

    print(fInternal_List_bool())

    def fInternal_List_Sum_Min_Max():
        setSet=[1,2,3]
        print(f" max setSet :{max(setSet)}")
        print(f" sum setSet :{sum(setSet)}")
        print(f" min setSet :{min(setSet)}")
        sStr="qwertz,as"
        print(f" max setSet :{max(sStr)}",
              f" min setSet :{min(sStr)}")
    fInternal_List_Sum_Min_Max()

#---------------------------Run Block
fExternal()