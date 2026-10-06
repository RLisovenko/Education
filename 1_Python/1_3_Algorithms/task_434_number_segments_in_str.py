import sys, math, numpy, string
from typing import Any
"""
        Description: Given a string s, return the number of segments in the string.
                     A segment is defined to be a contiguous sequence of non-space characters.
                     0 <= s.length <= 300
                     s consists of lowercase and uppercase English letters, digits, or one of the following characters "!@#$%^&*()_+-=',.:".
                     The only space character in s is ' '
                    keyboard key https://css-tricks.com/snippets/javascript/javascript-keycodes/
        Author:     RuslanLisovenko@gmail.com
        Date:       1508-2023        
"""
class Solution:       
    def __init__(self):
        self.clsSpace = chr(32)  # oder char(CodeSpace) print("'" + chr(32) + "'")         

    def funcCountSegments(self, sStr:str) -> int:
        """
        wie viele word in string
        :type s: str
        :rtype: int
        """
        clsSpace = chr(32)        
        iCountSeg = 0 #: sStr.count(clsSpace)
        #iCountSpaceDel = 0        
        iEndPosSeg = len(sStr) - sStr[::-1].find(clsSpace)
        #ss = sStr.split()
        return len(sStr.split()) # split word in string

        
        #if len(sStr) == sStr.count(clsSpace):
        #    return 0
        #elif len(sStr) >0 and sStr.count(clsSpace) == 0:
        #    return 1
        #elif iEndPosSeg < len(sStr):
        #    return iCountSeg + 1
        #elif iEndPosSeg == len(sStr):
        #    return iCountSeg
        #else:
        #    return iCountSeg
        
#------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 20. :")         
        sInput = str("Hello, my name is John")             

        clsObj_434 = Solution()        
        sInput = "    Of all the gin joints in all the towns in all the world,   "
        print("Sie haben segment: ",clsObj_434.funcCountSegments(sInput))
        
        while sInput != 'stop':
            sInput = str(input("Input string verglechen : "))
            if len(sInput) > 0 and len(sInput) <= 300:                               
                print("Sie haben segment\worter\words: ",clsObj_434.funcCountSegments(sInput))
                print("---------------------------------------------------------while - > Write/schreiben Sie bitte stop fur end iteration.:")
            else:
                print("Sehr lange string.")
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_434 = None

print("---------------------------------------------------------End von Aufgabe 20. : ")   