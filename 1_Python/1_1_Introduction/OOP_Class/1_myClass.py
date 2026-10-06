class myClass_1():
    #------machen atribute
    intValue = 9
    strValue="qwerty"
    pass
#---------------------
myObj_1 = myClass_1()
myObj_2 = myClass_1()
print(type(myObj_2))
print(myObj_1.intValue)
print(myObj_2.strValue)
myObj_1.intValue = 11
myClass_1.intValue = 12
print(myObj_2.intValue)
print(myObj_1.intValue)