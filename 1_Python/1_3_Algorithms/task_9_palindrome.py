import sys, math
from uu import Error
import numpy


"""
    Description 9:
        Given an integer x, return true if x is a palindrome , and false otherwise.
        example palindrome - tenet.-231 <= x <= 231 - 1
    Author: RuslanLisovenko@gmail.com
    Date:   1008-2023

"""
class Solution():
    def __init__(self, iXvalue: int):
            self.iXvalue = iXvalue            

    def IsPalindrome(self, x: int) -> bool:
        if x >= -1 * pow(2, 31) and x <= pow(2, 31) - 1:            
            if int(str(abs(x))[::-1]) == x:                
                return True
            else:             
                return False
        else:            
            return False
          

#-------------------------------------------------main
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 9.:")

        iXvalue = int(input("enter bitte Numeric int value: "))
        #print(int(str(iXvalue)[::-1]))
        if type(iXvalue) is int:
            myObj_9 = Solution #(iXvalue)
            bValue = myObj_9.IsPalindrome(iXvalue)
            if bValue is True:
                print("Das ist Value ist palindrome: ", bValue)
            else:
                print("Das ist Value ist keine palindrome: ", bValue)
        else:
            print("Type von obj Erorr. Input correct Value.",iXvalue)
    except TypeError:
        print("Sie haben ein Erorr + fehler - TypeError:",NameError)
    except ValueError:
        print("Sie haben ein Erorr + fehler - ValueError:",Error)
    finally :
        #Clear\putsen alle obj
        myObj_9 = bValue = None


print("---------------------------------------------------------End von Aufgabe 9.:")
    