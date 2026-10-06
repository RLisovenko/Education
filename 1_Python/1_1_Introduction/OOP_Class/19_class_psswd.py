class MyObj():
    def __init__(self):
        self.password = None
    def __getattribute__(self, item):
        if item == "secret_field" and self.password == "qwerty":
            return "Secret value"
        else:
            return object.__getattribute__(self, item)

#------start
obj_1 = MyObj()
obj_1.password = "qwerty            "
print(obj_1.secret_field)
