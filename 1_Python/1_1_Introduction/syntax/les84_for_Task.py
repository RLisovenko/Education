"""
#Comment
"""
sStr="Hallo Ukraine."
sResult=""
for sChar in sStr:
    if sChar=="o":
        sResult=sResult+'e'
    elif sChar=="l":
        sResult=sResult+'l'
    else:
        sResult=sResult+sChar
print(sResult)


