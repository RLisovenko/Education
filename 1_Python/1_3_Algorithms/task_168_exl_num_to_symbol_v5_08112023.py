        
#import sys, math, numpy, string
import pandas as pd
#import io, os
#from itertools import product
         
class Solution():
    """
                Description neu Ergebnise 
                     ab chr(48) bis 57 -> grosse 0....9
                     ab 65 bis 90 -> grosse ord(A)....Z
                     
                print(7/2)    # 3.5 - обычное математическое деление          
                print(9//2)   # 4 - целочисленное деление
                print(7%2)    # 1 - остаток от деления
                        #List = [a,s,d,f,g]
                        #--------dDict_1={'key1':'ein','key2':2}
                        #--------sStr='qwerty'            
                        #cortage = (1,2,3)
                Author:     RuslanLisovenko@gmail.com                   
                Date:       0811-2023     
    """  
    def __init__(self):
        pass
  
    def convertToTitle(self, columnNumber: int) -> str:

        sResultNumColumnToCharCol = []
        sNextSymbol = None        

        while columnNumber > 0:   
            #sNextSymbol = chr(64 + (columnNumber//26))
            iRes = columnNumber % 26
            sNextSymbol = chr(65 + (columnNumber - 1) % 26)
            sResultNumColumnToCharCol.append(sNextSymbol)
            columnNumber = (columnNumber - 1) // 26

        sResultNumColumnToCharCol.reverse()

        return "".join(sResultNumColumnToCharCol)
#-------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        sResult = ""
        iColNum = 64
        for iCodeChar in range(64, 90 + 2): # ab 65 bis 90 muss                                
            sResult = chr(iCodeChar)
            print(f" Column:{iColNum} -> ", sResult)
            iColNum += 1

        #print("---------------------------------------------------------Start von Aufgabe 168. :") 
        obj168 = Solution()
        for iNumCol in range(0, 1000):
            print(f"Column{iNumCol}: ->to char-> {obj168.convertToTitle(iNumCol)}")

        #print("---------------------------------------------------------end von Aufgabe 168. :") 
    except:
         pass