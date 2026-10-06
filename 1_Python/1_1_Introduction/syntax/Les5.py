iNum=0
#--------------------ich mache----
cVar=input('Input eine  Numer:-')
#sStrTypeVar=type(cVar)
#str.isdecimal() -Return True if all characters in the string are decimal characters
#str.isdigit() - Return True if all characters in the string are digits
#str.isnumeric() - Return True if all characters in the string are numeric characters
#str.isprintable()  - Return True if all characters in the string are printable or the string is empty
if cVar.isdigit()==False:
    print("Sie schreiben string:","Error type Numer")
elif cVar==0:
    print("Error entritt , bitte andere Num", "Andere Num, aber nicht 0")
elif len(cVar)==0:
    print("Sie NICHT schreiben string:", "Error type Numer")
else:
    iNum0=float(cVar)
#-----------------macht Lehrer--------zaluschok ot delenia
    if iNum % 2 :
        #if ostatok ==0 dan true das bedeitet paar
        print('Das ist Numer ist kein paarne',iNum0)
    else:
        # if 0 dan false
        print('Das ist  paar',iNum0)

