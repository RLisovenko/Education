"""
import Module
import module_name as Newname
"""
def myGen_Fib(iCount = 10):
    num_1, num_2 , ii = 0, 1, 0
    while True:
        #print(num_2)
        yield num_2
        num_1, num_2 = num_2 , num_1 + num_2
        if ii <= iCount:
            ii += 1
        else:
            break
    print("end iteration:",iCount)

def my_fib_new(limit):
    myGenValue = myGen_Fib()
    for _ in range(limit):
        yield (next(myGenValue))

def my_fib_Return_Num(welheNumFib):
    result = None
    for currentNum in my_fib_new(welheNumFib):
        result = currentNum
    return result

if __name__ == "__main__":
    print("Start test",my_fib_Return_Num(11))
    assert(my_fib_Return_Num(11))