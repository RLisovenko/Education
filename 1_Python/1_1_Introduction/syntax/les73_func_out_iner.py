"""
__name__
dir() - welhe func un var ist
#функция показвает что в глобал и внутреней части Пайтон берет поочереди вверх
сначала береться локально потом выше и выше, это про переменые
"""

iVarOuter=0
def fOuter():
    iVarOuter=1
    def fInner():
        print(f"Print {iVarOuter}")
    fInner()
    iVarOuter=2

    print(f"Print {iVarOuter}")
    fInner()
fOuter()