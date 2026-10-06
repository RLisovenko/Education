import sys, math
from uu import Error
import numpy


"""
    Description 869:
                You are given an integer n. We reorder the digits in any order (including the original order) such that the leading digit is not zero.
                Return true if and only if we can do this so that the resulting number is a power of two.
    Constraints:1 <= n <= 10^9  ->    2 4 8 16 32 64 128.....
    Author:     RuslanLisovenko@gmail.com
    Date:       1008-2023
"""
class Solution():
    def __init__(self, iNvalue: int):
            self.iNvalue = iNvalue
    
    def funcReorderedPowerOf2(self, iNvalue = 0) -> bool:          

          if iNvalue >= 1  and iNvalue <= pow(10, 9):   
            Result = 0 
            iNRange2Pow = 0
            #strList = list(['1',])
            for _ in range(pow(10, 9)):
                Result = pow(2,iNRange2Pow)
                if len(str(Result)) == len(str(iNvalue)):
                    if iNvalue == Result: return True

                    iValueSorted  = sorted(str(iNvalue))
                    iValueSorted = "".join(iValueSorted)                
                    if iValueSorted == Result: return True

                    Result  = sorted(str(Result))
                    Result = "".join(Result)
                    if iValueSorted == Result: return True                  

                elif iNvalue <  Result:
                    break                
                iNRange2Pow += 1

            return False            
                
          else:
            print("Out of Range: ", iNvalue)
            return False 
          #-------------------------------------------------------------------------  
          #print(f"Range Value power von 2", strList)                      
          
          
#-----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 869.:")      
        
        iNvalue = int(input("enter bitte Numeric int value in range 1 <= n <= 109 : "))
        clsObj_869 = Solution(iNvalue)           
        boolResultPowerOf2  = clsObj_869.funcReorderedPowerOf2(iNvalue)

        print(f"funcReorderedPowerOf2: Diese Value = {iNvalue} ist {boolResultPowerOf2} power von 2: ",boolResultPowerOf2,iNvalue)                                                        
    except:
         print("Sie haben eine Error:",Error)
    finally:
         clsObj_869 = iNvalue = None

print("---------------------------------------------------------End von Aufgabe 869.:")



