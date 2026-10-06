class my_ClassObj_13():
    class_attribute = 8
    def __init__(self):
        self.data_attribute = 88
    def instance_method(self):
        print("attribute in __init__",self.data_attribute)

    # call kan in class und in exemplar class
    @staticmethod
    def myStatic_method():
        print("change class attribute via @staticmethod: ",my_ClassObj_13.class_attribute)

if __name__ == "__main__":
    my_ClassObj_13.myStatic_method()
    myObj = my_ClassObj_13()
    myObj.instance_method()
    myObj.myStatic_method()