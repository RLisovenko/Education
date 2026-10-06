class my_class_obj_property():
    def __init__(self):
        self.__attribute = 0

    @property
    def my_Attribute(self):
        return self.__attribute
    @my_Attribute.setter
    def my_Attribute(self, myNewValue):
        if myNewValue < 100:
            self.__attribute = myNewValue


# -------------------

myObject = my_class_obj_property()
print(myObject.my_Attribute)
myObject.my_Attribute = 99
print(myObject.my_Attribute)
#--------oder
print(myObject._my_class_obj_property__attribute)
print(my_class_obj_property.my_Attribute)
