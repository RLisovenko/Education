"""
python app_scriprt.py "argument modul"
__init__.py
"""
import os.path
import sys
import les71_fib as myModuleFib

if __name__ == '__main__':
       pass

#добавляет мли проекті в глобальніе переменніе python

myCurrent_path = os.path.dirname(os.path.abspath(__file__))
myParent_path = os.path.dirname(myCurrent_path)
#my_module_path = os.path.join('..',"Vss")
my_module_path = os.path.join(myParent_path,"Vss")
sys.path.append(my_module_path)
print(my_module_path)
print("sys.argv: ",sys.argv)
print("sys.path: ",sys.path)
print("__file__: ",__file__)
print("__main__: ",__name__)
print("-" * 48)
print(myModuleFib.my_fib_Return_Num(10))

