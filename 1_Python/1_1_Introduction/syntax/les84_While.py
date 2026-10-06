
cVar=9
bVar=True
#-----------
while bVar==True:
#break
#continue
    cVar-=1
    if cVar==-9:
        bVar = False
    elif cVar==3:
        continue
    elif cVar==-3:
        continue
        #break
    else:
        bVar=True
    print(cVar)
else:
    print("print End loop end:",cVar)