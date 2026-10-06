sList_All=['a','b','c','d']
sList_Num1=[1,2,3,4]
sList_Num2=[4,3,2,1]
print(type(sList_All))
print(type(sList_Num2))
print(sList_Num1==sList_Num2)

fFunc=[print,len,type]
for i in fFunc:
    for k in sList_All:
        print('Result:',i(k))
print(sList_All[1:5:2])
#Spiegel fur List
print(sList_All[::1])
print(sList_All[::-1])

#Spiegel fur string
sStr='qwerty'
print(sStr[::1])
print(sStr[::-1])#'obratnay invertir str
#---------------------------------------------------
sList_All_Copy=sList_All[:] #create variable als
print (sList_All is sList_All_Copy) #fur varibale List return False
sList_All_Copy =3*(sList_All_Copy+sList_All[::-1])
print(sList_All_Copy)
print(len(sList_All_Copy))
print(min(sList_All_Copy))
sList_All_Copy='ab'+'ba'
print(sList_All_Copy)
print(min(sList_All_Copy))
print(max(sList_All_Copy))
#-----------------------
sStr_Copy=sStr[:]
print(sStr_Copy is sStr) #fur str true return
sStr_Copy=2*(sStr_Copy+sStr[::-1])
print(sStr_Copy)
print(len(sStr_Copy))
#-------------------------List Numbers
iNumbers_List=[1,3,44,88,9,123]
iNumbers_List[1]=2
print(iNumbers_List)
del(iNumbers_List[-2])
print(iNumbers_List)
#------------------------------------
sList_All_Copy=['begin','re',"as",'fg','zu','ukr','end']
sList_All_Copy[1:3]=iNumbers_List
print(sList_All_Copy)
#-------------------------------------------
sList_All_Copy+=sList_All_Copy
sList_All_Copy+=[1,2,3]
sList_All_Copy=[3,6,9]+sList_All_Copy
print(sList_All_Copy)
sList_All_Copy[3:6]=[] # add empty str
sList_All_Copy+=[20]
#-------------------Distc
dDict_1={'key1':'ein','key2':2}
print(dDict_1['key1'])
print(dDict_1['key2'])
dDict_1['key3']=[3,3,3]
print(dDict_1)
print(dDict_1.items())
print(dDict_1.keys())
print(dDict_1.values())
dDict_2=dDict_1
print(type(dDict_1))
print(dDict_1.update(dDict_2))
#------------------------class - SET
vVar=set('qwertz')
vVar1={'6','5','3','4'}
vVar2= {'4','5','6'}
print(type(vVar))
print(vVar)
print(type(vVar1))
print(vVar1)
vVar1.add('1')
print('union=',vVar1.union(vVar2))
print('intersection=', vVar1.intersection(vVar2))
print('difference=',vVar1.difference(vVar2))
print("vVar1-vVar2=",vVar1-vVar2)
vVar1.remove('1')
print("vVar1-vVar2=",vVar1-vVar2)
vVar1.discard('3')
print("vVar1-vVar2=",vVar1-vVar2)
vVar1.add('777')
print("vVar1-vVar2=",vVar1-vVar2)