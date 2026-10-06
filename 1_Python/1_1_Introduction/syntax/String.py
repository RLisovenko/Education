sStr='Das ist ersten Line'
sErr="Das ist ein Fehle/ Error-"
iCount=0
bBool=False
cVar="Complex variables"
#------------------------------------
print("Erorr-",sStr)
print("Slasch \\")
print("Print Tab \t Tab")
print("Print",{sStr})
sRaw=r"qwertz \  йцукен - "+sStr
print(sRaw)
print('-'*80)
sUkr="qwertzasqwertz"
sResult="as" in sUkr
print ("Result",sResult)
print(sUkr[6]+sUkr[7]+sUkr[7:9]+sUkr[1:10:3])
print(sResult)
print(sUkr.upper())
#-------------------------------
iCount=sStr.count
print("length-",iCount)
sUkr=sStr.upper()
print("upper-",sUkr)
print("Type cVar",type(cVar))
if type(cVar)=='str':
    cVar=sUkr.str()
    print("New cVar",cVar)
else:
    print("Prn sUkr",sUkr)

print("Returns a string representation of an object-",cVar)
bBool="as" in sUkr
print("Operator 'in' -",bBool)