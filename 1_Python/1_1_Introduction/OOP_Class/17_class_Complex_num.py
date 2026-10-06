"""
__doc__
Complex num das ist sum zwei num
левая часть целое число
правое произведение действительного на
произведение на 1
myNumImaginary = мнимое число
"""
class myClassComplex:
    def __init__(self,myNumReal = 0.0, myNumImaginary = 0.0):
        self.NumClass_Real = myNumReal
        self.NumClass_Imaginary = myNumImaginary
    def __repr__(self):
        return "myClassComplex({!r}, {!r})".format(self.NumClass_Real,self.NumClass_Imaginary)
    def __str__(self):
        return "{}{:+d}i".format(self.NumClass_Real,self.NumClass_Imaginary)
    def __add__(self,myOtherNum):
        return myClassComplex(self.NumClass_Real + myOtherNum.NumClass_Real, self.NumClass_Imaginary + myOtherNum.NumClass_Imaginary)
    def __neg__(self):
        return -self.NumClass_Real, -self.NumClass_Imaginary
    def __sub__(self, other):
        return (self + (-other))
    def __abs__(self): # modul num
        return (self.NumClass_Real ** 2 + self.NumClass_Imaginary) ** 0.5
#---------start
print(myClassComplex(3,5))
#-------------add
print(myClassComplex(3,5) + myClassComplex(2,-1))
print(-myClassComplex(3,5))
#---------sub
print(myClassComplex(4, 2) - myClassComplex(2, 1))
#-------modul
print(abs(myClassComplex(3,5)))