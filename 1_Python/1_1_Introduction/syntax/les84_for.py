#py nicht     for(i=1;i<=10;i++):
sStr="HAllo Ukraine"
iterator_Var=iter(sStr)
#----------------------------------
for cVar in sStr:
    print(cVar)#+' '+type(iterator_Var))
    print(type(iterator_Var))
next(iterator_Var)
#StopIteration

print("cVar:",iter(cVar))
print("sStr",iter(sStr))
#-----------------------------------range coolation
iStep=3
collation_Var=range(3,33,iStep)
# from 3 bis 33 mit step 3
for cVar in collation_Var:
    print(cVar)
    #Break else nicht machen
    #continue das func mache next iteration
else:
    print("Done will execute")


