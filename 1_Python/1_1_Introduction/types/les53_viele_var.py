def myFunc(x,*args):
    print(f"x={x}")
    print("andere args = ", args)
    return args
def myF_math(first_arg,*vile_numbers):
    mySum = first_arg  +sum(vile_numbers)
    return  mySum / (len(vile_numbers) + 1)

myValue = myFunc(2,3,5,6,7)
print(*myValue)
print(*myValue,sep= ";")
print("sum mit ",myF_math(1,2,3,4,5,6,7))
