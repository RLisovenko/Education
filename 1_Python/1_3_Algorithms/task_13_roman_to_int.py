import io, os
import sys, math, numpy, string
from typing import Any
import pandas as pd
import itertools

"""
    Description file:   Roman numerals are usually written largest to smallest from left to right. However, the numeral for four is not IIII. Instead, the number four is written as IV. Because the one is before the five we subtract it making four. The same principle applies to the number nine, which is written as IX. There are six instances where subtraction is used:
                        I can be placed before V (5) and X (10) to make 4 and 9. 
                        X can be placed before L (50) and C (100) to make 40 and 90. 
                        C can be placed before D (500) and M (1000) to make 400 and 900.
                        Given a roman numeral, convert it to an integer.
                        Symbol       Value
                        I             1
                        V             5
                        X             10
                        L             50
                        C             100
                        D             500
                        M             1000               
    Constraints: 1 <= s.length <= 15
                 s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M').
                 It is guaranteed that s is a valid roman numeral in the range [1, 3999].
    Author:     RuslanLisovenko@gmail.com
    Date:       1408-2023
"""
class Solution:
    """
    #List = [a,s,d,f,g]
            #--------dDict_1={'key1':'ein','key2':2}
            #--------sStr='qwerty'            
            #cortage = (1,2,3)
    """
    def __init__(self,*arg):                     
            #self.dictIntToSymbol = {1: 'I', 5:'V', 10:'X', 50:'L', 100:'C', 500:'D', 1000:'M'}
            #self.dictSymbolToInt = {'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10, 'XL': 40, 'L': 50, \
            #                        'XC': 90, 'C': 100, 'CD': 400, 'D': 500,'CM': 900, 'M': 1000}            
            pass
    def romanToInt(self, sSymbolInRoman: str) -> int:

        iBegRange = 1 
        iEndRange = 3999
        sSympolToInt=['I','V', 'X', 'L', 'C','D','M']
        #dictIntToSymbol = {1: 'I', 5:'V', 10:'X', 50:'L', 100:'C', 500:'D', 1000:'M'}
        

        """
            I can be placed before V (5) and X (10) to make 4 -> IV and 9 -> IX. 
            X can be placed before L (50) and C (100) to make 40 -> XL and 90->XC
            C can be placed before D (500) and M (1000) to make 400 -> CD and 900 ->CM
        """
        iValueInInt = 0
        #while len(sSymbolInRoman) !=0:
        for _ in range(len(sSymbolInRoman)):

            if "IV" in sSymbolInRoman: #4
                iCountSymbol = sSymbolInRoman.count("IV")
                iValueInInt = iValueInInt +  self.methGetDigitVal("IV") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("IV"," ")            

            if "IX" in sSymbolInRoman: #9
                iCountSymbol = sSymbolInRoman.count("IX")
                iValueInInt = iValueInInt +  self.methGetDigitVal("IX") * iCountSymbol 
                sSymbolInRoman = sSymbolInRoman.replace("IX","")    

            if "XL" in sSymbolInRoman: #40
                iCountSymbol = sSymbolInRoman.count("XL")
                iValueInInt = iValueInInt +  self.methGetDigitVal("XL") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("XL","")  

            if "XC" in sSymbolInRoman: #90
                iCountSymbol = sSymbolInRoman.count("XC")
                iValueInInt = iValueInInt +  self.methGetDigitVal("XC") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("XC","") 

            if "CD" in sSymbolInRoman: #400
                iCountSymbol = sSymbolInRoman.count("CD")
                iValueInInt = iValueInInt +  self.methGetDigitVal("CD") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("CD","")

            if "CM" in sSymbolInRoman: #900:
                    iCountSymbol = sSymbolInRoman.count("CM")
                    iValueInInt = iValueInInt + self.methGetDigitVal("CM") * iCountSymbol * iCountSymbol
                    sSymbolInRoman = sSymbolInRoman.replace("CM","")

            if "I" in sSymbolInRoman: #1
                iCountSymbol = sSymbolInRoman.count("I")
                iValueInInt = iValueInInt +  self.methGetDigitVal("I") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("I","")
                       
            if "V" in sSymbolInRoman: #5
                iCountSymbol = sSymbolInRoman.count("V")
                iValueInInt = iValueInInt +  self.methGetDigitVal("V") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("V","")

            if "X" in sSymbolInRoman: #10
                iCountSymbol = sSymbolInRoman.count("X")
                iValueInInt = iValueInInt +  self.methGetDigitVal("X") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("X","")

            if "L" in sSymbolInRoman: #50
                iCountSymbol = sSymbolInRoman.count("L")
                iValueInInt = iValueInInt +  self.methGetDigitVal("L") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("L","")

            if "C" in sSymbolInRoman: #100
                iCountSymbol = sSymbolInRoman.count("C")
                iValueInInt = iValueInInt +  self.methGetDigitVal("C") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("C","")

            if "D" in sSymbolInRoman: #500
                iCountSymbol = sSymbolInRoman.count("D")
                iValueInInt = iValueInInt +  self.methGetDigitVal("D") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("D","")            

            #----------------------------------------------------         
            if "M" in sSymbolInRoman: #1000 -
                iCountSymbol = sSymbolInRoman.count("M")                
                iValueInInt = iValueInInt + self.methGetDigitVal("M") * iCountSymbol
                sSymbolInRoman = sSymbolInRoman.replace("M","")
             
            if len(sSymbolInRoman) ==0 : 
                break
            else:
                continue

        return iValueInInt

    def methGetDigitVal(self, sSymbol: str) -> int:
        dictSymbolToInt = {'I': 1, 'IV': 4, 'V': 5, 'IX': 9, 'X': 10, 'XL': 40, 'L': 50, \
                            'XC': 90, 'C': 100, 'CD': 400, 'D': 500,'CM': 900, 'M': 1000}                    
        return dictSymbolToInt[sSymbol]
#------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 13.:") 
        clsObj_13 = Solution()
        print("---------------------------------------------------------Parsing Int to Roman .:") 
        print("value1:    ",clsObj_13.funcIntToRoman(1))        
        print("Value5:    ",clsObj_13.funcIntToRoman(5))
        print("Value50:   ",clsObj_13.funcIntToRoman(50))
        print("Value55:   ",clsObj_13.funcIntToRoman(50))
        print("Value100:  ",clsObj_13.funcIntToRoman(100))
        print("Value111:  ",clsObj_13.funcIntToRoman(111))
        print("Value1111: ",clsObj_13.funcIntToRoman(1111))

        print("Value255:  ",clsObj_13.funcIntToRoman(255))
        print("Value1255: ",clsObj_13.funcIntToRoman(1255))
        print("Value2255: ",clsObj_13.funcIntToRoman(2255))
        print("Value3255: ",clsObj_13.funcIntToRoman(3255))
        print("Value3999: ",clsObj_13.funcIntToRoman(3999))

        print("---------------------------------------------------------Parsing Roman to int .:")
        print("value I:    ",clsObj_13.funcRomanToInt('I')) 
        print("value V:    ",clsObj_13.funcRomanToInt('V')) 
        print("value X:    ",clsObj_13.funcRomanToInt('X'))        
        print("Value L:    ",clsObj_13.funcRomanToInt('L'))
        print("Value C:   ",clsObj_13.funcRomanToInt('C'))
        print("Value D:   ",clsObj_13.funcRomanToInt('D'))
        print("Value M:  ",clsObj_13.funcRomanToInt('M'))       

        print("---------------------------------------------------------Parsing Roman to int .:")
        
        #print("Value CXI -> 111:  ",clsObj_13.funcRomanToInt('CXI')) 
        #print("Value MCXI -> 1111:  ",clsObj_13.funcRomanToInt('MCXI')) 
        #print("Value CCLV -> 255:  ",clsObj_13.funcRomanToInt('CCLV'))
        #print("Value MCCLV -> 1255:  ",clsObj_13.funcRomanToInt('MCCLV'))
        #print("Value MMCCLV -> 2255:  ",clsObj_13.funcRomanToInt('MMCCLV'))
        #print("Value MMMCCLV -> 3255:  ",clsObj_13.funcRomanToInt('MMMCCLV'))
        #print("Value MMMCCCCCCCCCLXXXXVIIII->3999:  ",clsObj_13.funcRomanToInt('MMMCCCCCCCCCLXXXXVIIII'))

        sSymbol = ''
        while sSymbol != 'stop' :
            #sSymbol = str(input("Enter Roman value , als char  Sympo =['I','V', 'X', 'L', 'C','D','M']: "))
            if len(sSymbol) <=15:
                #print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))
                sSymbol = "CDIV"
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))
                sSymbol = 404              
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcIntToRoman(sSymbol))

                sSymbol = 2399              
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcIntToRoman(sSymbol))
                sSymbol = "MMCCCXCIX"
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))

                sSymbol = 1476              
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcIntToRoman(sSymbol))
                sSymbol = "MCDLXXVI"
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))

                sSymbol = 2216              
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcIntToRoman(sSymbol))
                sSymbol = "MCMXCIV"
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))
                
                sSymbol = 1994
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcIntToRoman(sSymbol))
                sSymbol = "MDCCCCLXXXXIIII"
                print(f"Value {sSymbol} -> ist int: ",clsObj_13.funcRomanToInt(sSymbol))

                #print("Write/schreiben Sie bitte stop fur end iteration.")
                print("---------------------------------------------------------while - > Write/schreiben Sie bitte stop fur end iteration.:")
            else:
                print("Enter bitte sSymbol bis 15 len.")
                break
            
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_13 = None

print("---------------------------------------------------------End von Aufgabe 13.:")       