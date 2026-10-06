class my_Class_Obj():
    def __init__(self):
        self.__private_attribute = 48
    def get_Attr(self):
        return self.__private_attribute
    def set_attr(self,myValue):
        if myValue < 100:
            self.__private_attribute = myValue
#-------------------Start alt+schift_F5
myObj = my_Class_Obj()
print(myObj.get_Attr())
#или доступ напрямую к атрибуту каласса
print(myObj._my_Class_Obj__private_attribute)