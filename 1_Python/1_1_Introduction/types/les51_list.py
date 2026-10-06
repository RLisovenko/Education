"""
List = [a,s,d,f,g]
cortage = (1,2,3)
str = "qwerty"
"""
import collections.abc
myList = [1,2,3,4,5,6]
myList_2 = list(x ** 2 for x in range(10))


print(myList[2])
print(myList.__getitem__(2))
print(myList[2:6:1])
print(myList.index(5, 2 ))
print(  myList.count(5 ))
print(myList_2)
print(myList_2.sort)
#print(myList_2.sort(reverse = True ))
#print(myList_2.reverse())
print(ord('A'))
myList_3 = "asdfgWQWERTT"
print(myList_3.casefold)
