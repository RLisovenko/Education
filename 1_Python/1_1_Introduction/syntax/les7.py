#Funct fur Numeric

fNum=int(input("Input ein Numeric :"))
sSign="Numeric ist : '+'" if fNum>0 else "Numeric ist: '-'"
#print("Znak-",sSign)

if fNum==0:
    print(f"Var =0 Non habe Znak!",fNum)
else:
    if len(str(abs(fNum)))==1:
        print(f"Ein Znak {sSign}",fNum)
        #f-stroka
    elif len(str(abs(fNum))) == 2:
        print(f"Zwei Znak {sSign}",fNum)
    elif len(str(abs(fNum))) == 3:
        print(f"Drei Znak {sSign}",fNum)
    else:
        print(f"Viele Znak haben das Numerik: {sSign}",fNum) # f-stroka