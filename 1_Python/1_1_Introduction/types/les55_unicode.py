from keyword import iskeyword

myStr = u"український \n\t текст"
print(myStr)

print(myStr.upper())
print("myStr.count(т)",myStr.count("т"))
print(myStr.join(u"т"))
print(myStr.ljust(2,"y"))
print(myStr.replace(u"текст","text"))


myTuple = (1,)
myList = [1,2,3,4]
print("myTuple == myList->",myTuple == myList)
print("myTuple == myStr->", myTuple == myStr)
print("myTuple == myStr->", myList == myStr)