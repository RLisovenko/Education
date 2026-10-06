class clsSingl():
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)

        return cls._instance
    def __init__(self):
        self.value = "Hallo some value"
#-----------start
obj_1 = clsSingl()
obj_2 = clsSingl()
print(obj_1)
print(obj_2)
print(obj_1.value)