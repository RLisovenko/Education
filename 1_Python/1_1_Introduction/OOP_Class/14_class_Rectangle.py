class myClassRectangle():
    def __init__(self, side_a, side_b):
        self.side_a = side_a
        self.side_b = side_b
    def __repr__(self):
        return "myClassRectangle(%.1f, %.1f)" % (self.side_a,self.side_b)
class myClassCircle():
    def __init__(self, radius):
        self.radius = radius
    def __repr__(self):
        return ("myClassCircle %.1f" % self.radius)
    #@staticmethod def my_Circle_from_Rectangle(selfrectangle):
    #return myClassCircle(radius) возращается єкземпляр єтого єе класса
    #---------------------
    # oder  @classmethod def my_Circle_from_Rectangle(cls,selfrectangle):
    # classmethod если возращаем неизвестный класс внутри другого класса
    @classmethod
    def my_Circle_from_Rectangle(cls, rectangle):
        radius = (rectangle.side_a ** 2 + rectangle.side_b ** 2) ** 0.5 / 2
        return cls(radius)
def myFuncMain():
    myRectangle_1 = myClassRectangle(3,4)
    print(myRectangle_1)
    myCircle_1 = myClassCircle(1)
    print(myCircle_1)
    myCircle_2 = myClassCircle.my_Circle_from_Rectangle(myRectangle_1)
    print(myCircle_2)

#--------------------------------
if __name__ == "__main__" :
    print(__name__)
    myFuncMain()
else:
    myFuncMain()
