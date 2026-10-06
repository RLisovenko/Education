class my_class_Person():
    def __init__(self, name, age):
        """"
        init first start und insialise variable
        """
        self.name = name
        self.age = age

    def myPrn_info_Person(self):
        print(self.name, " ist ", self.age ,"Jahre alt")

#---------------machen datei von class------------

myObjMan = my_class_Person("Ruslan",48)
#myObjFrau = my_class_Person("Olena",40)
myObjFrau = my_class_Person
myObjFrau.name = "Olena"
myObjFrau.age = "40"

print("Type obj: ",myObjMan)
print(f"{myObjMan.name}({myObjMan.age} Jahre Alt) + {myObjFrau.name}({myObjFrau.age} jahre alt) ist eine Ehepaar", )

myObjFrau.myPrn_info_Person
myObjMan.myPrn_info_Person
print("-----------verschidene call")
myObjFrau.myPrn_info_Person

my_class_Person.myPrn_info_Person(myObjMan)

print("---------Type--------------")
print("Type class",type(my_class_Person))
print("Type DataItems class",type(myObjFrau))
print("Type MethodClass",type(myObjFrau.myPrn_info_Person))

#------------Example fur init varible von class


