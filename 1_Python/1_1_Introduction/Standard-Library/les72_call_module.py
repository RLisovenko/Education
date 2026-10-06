import les71_fib  as myModuleName

"""
python app_scriprt.py "argument modul"

import Module
import module_name as Newname
from   module_name import *
from   module_name import name1 as NewName1,name2 as  NewName2
"""


print(myModuleName.__name__)
indexFib = int(input("enter num von Fib:"))
print(myModuleName.my_fib_Return_Num(indexFib))