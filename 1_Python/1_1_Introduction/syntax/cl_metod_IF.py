iNum1=1
iNum2=100
iNum0=0
sAlt="Non Findet Jahre Alt"
#-------------------------
if iNum1>iNum2:
    print("Var iNum1>iNum2:",iNum1-iNum2)
if iNum0:
    print("Resut iNum0-",bool(iNum0))
elif iNum2:
    print("Resut iNum2-", bool(iNum2))
else:
    print("Resut iNum1-",bool(iNum1))
#Andere benutctnen - use
if iNum0 : print("If true mache viele Aufgabe fur 0-","Task0"); print("Aufgabe 0 -N-","TaskN")
elif iNum1 : print("If true mache viele Aufgabe fur 1-","Task1"); print("Aufgabe 1 -N-","TaskN")
else: print("If true mache viele Aufgabe fur 2-","Task2"); print("Aufgabe 2 -N-","TaskN")
#----------3 Variant using
print("Prn iNum0 -",iNum0) if iNum2>=100 else print("Prn iNum1 -",iNum1)
#----------4 Variant using
sAlt='Junge' if iNum2>12 else 'Man'
print("Welhe Jare alt :",sAlt)