import io, os
import sys, math, numpy, string
from typing import Any
import pandas as pd

"""
    Description file: Given an integer n, return true if it is a power of three. Otherwise, return false.
                      An integer n is a power of three, if there exists an integer x such that n == 3x.                
                     -231 <= n <= 231 - 1
    Author:     RuslanLisovenko@gmail.com
    Date:       0911-2023
"""

class Solution:
    def isPowerOfThree(self, n: int) -> bool:
        
        if n in self.methSetListPow():
            return True
        else:
            return False 

    def methSetListPow(self) -> list:        
        iBeg = -1 * pow(2,31)
        iEnd = pow(2,31) - 1
        ListInRange = []
        iCountPowBeg = self.getiCountOfPowAnyNum(iBeg)
        iCountPowEnd = self.getiCountOfPowAnyNum(iEnd)
        #----------------Range vor 0
        #if iBeg < iEnd and iBeg < 0:          
        #    for iValue in range(1,iCountPowBeg + 1):   
        #        ResPowOfVar = -1 * pow(3, iValue)
        #        if ResPowOfVar >= iBeg and ResPowOfVar <= iEnd: 
        #            ListInRange.append(ResPowOfVar)            
        #----------------Range nach 0
        for iValue in range(0,iCountPowEnd + 1):       
                ResPowOfVar = pow(3, iValue)
                if ResPowOfVar >= iBeg and ResPowOfVar <= iEnd:  
                    ListInRange.append(ResPowOfVar)                                           

        return ListInRange

    def getiCountOfPowAnyNum(self, iNumforGetPow :int) -> int:        
            iCountPow = 1                
            iPowNum = 3
            iNextResult = iNumforGetPow / iPowNum       

            while abs(iNextResult) > iPowNum:                 
                iNextResult = iNextResult / iPowNum       
                iCountPow += 1

            return iCountPow

#------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 168.:")       
    
    except:
        print("Sie haben eine Error:")
        pass
    finally:
        clsObj_326 = None

print("---------------------------------------------------------End von Aufgabe 168.:")       