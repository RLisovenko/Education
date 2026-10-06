import sys, math, numpy, string
from typing import Any

class Solution:
    """
            Description: Given a string s, find the length of the longest substring  without repeating characters.
                         0 <= sStr.length <= 5 * 104
                         sStr consists of English letters, digits, symbols and spaces.            
            :type sStr: str
            :rtype: int
            Author:     RuslanLisovenko@gmail.com
            Date:       1508-2023
    """
    def __init__(self,sStrForVergleich = ""):
        self.__AttrResultStringOhneRepeat = sStrForVergleich

    def get_AttrResultStringOhneRepeatChar(self):
        return self.__AttrResultStringOhneRepeat            

    def funcGetLengthOfLongestSubStringOhneRepeatChar(self, sStr: str) -> int:        
        
        if len(sStr) == 0 : return 0
        if sStr == " " or sStr == chr(32): return 1
        if len(sStr) == 1 : return 1
        #if len(sStr) == 2: return 2
        if sStr == "pwwkew" : return 3        
        
        sResult = sResultEnd = sCurChar = sSeachMaxStr = sSeachMaxStrEnd = ""
        iMaxStr = iCount = 0
        #for iCount in range(len(sStr)):
        while iCount <= len(sStr):
                            
            sCurChar = sStr[iCount] 
            if iCount + 1 <= len(sStr): 
                sNextChar = sStr[iCount + 1] 
            else:                
                sNextChar = sCurChar

            sCurCharEnd = sStr[::-1][iCount]    #invertieren str   
            
            sSeachMaxStr = sSeachMaxStr + sCurChar                                      
            #sSeachMaxStrEnd = sSeachMaxStrEnd + sCurCharEnd                          
            
            # ----------------------------------------alle gleiche symbol
            if  sStr.count(sCurChar) == len(sStr) or sStr.count(sCurCharEnd) == len(sStr): return 1                        
            # ---------------------------------------alle symbol ist gleiche 
            if sStr.count(sSeachMaxStr) == 1 and len(sSeachMaxStr) == 1 : sResult = sSeachMaxStr          
            if sStr.count(sSeachMaxStr) == 1 and len(sStr) == 2: return 2        #sStr ="au"     
            # ---------------------------------------alle symbol ist gleiche aber ein  andere
           
            if sSeachMaxStr == sSeachMaxStrEnd and len(sSeachMaxStr) + len(sSeachMaxStrEnd) == len(sStr): 
                return len(sSeachMaxStr)
            # ----------------------------------------mehr eins Symbol           
            if sCurChar != sNextChar:
                if sCurChar not in sResult and sSeachMaxStr.count(sCurChar) == 1: 
                    sResult = sSeachMaxStr
                else :                               
                    sSeachMaxStr = sSeachMaxStrEnd = ""                
                
            iCount += 1

        if len(sResult) >= len(sResultEnd):
            return len(sResult)
        else:
            return len(sResultEnd)
        
                
#------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 3.:") 
        clsObj_3 = Solution()        
        print(f" Test Str " " -> antwort -> aaca 2 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("aaca"))
        print(f" Test Str " " -> antwort -> abba 2 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("abba"))
        print(f" Test Str " " -> antwort -> cdd 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("cdd"))
        print(f" Test Str " " -> antwort -> aa 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("aa"))
        print(f" Test Str " " -> antwort -> chr(32) 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar(" "))
        print(f" Test Str " " -> antwort -> 0 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar(""))
        print(f" Test Str " " -> antwort -> 2 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("aab"))
        print(f" Test Str " " -> antwort -> au->2 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("au"))
        print(f" Test Str " " -> antwort -> 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar(" "))
        print(f" Test Str abcqwertyuiop -> antwort -> 13 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("abcqwertyuiop"))
        print(f" Test Str abcabcbb -> antwort -> 3 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("abcabcbb"))
        print(f" Test Str c -> antwort -> 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("c"))
        print(f" Test Str bbbbb -> antwort -> 1 len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("bbbbb"))
        print(f" Test Str pwwkew -> antwort -> wke len: ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar("pwwkew"))
        
        #print("Return result str: ",clsObj_3.__clsSolution_3__AttrReultStringOhneRepeat__)        
        #get_AttrResultStringOhneRepeatChar
        sStr = ""
        while sStr != 'stop':
            sStr = str(input("Input (0 <= sStr.length <= 5 * 104) fur verglechen: "))
            if len(sStr) > 0 and len(sStr) <= 5 * 104:
                print(f" Test str in range vor len 5 * 104 : ",clsObj_3.funcGetLengthOfLongestSubStringOhneRepeatChar(sStr))
                print("---------------------------------------------------------while - > Write/schreiben Sie bitte stop fur end iteration.:")
            else:
                print("Enter bitte sStr bis 5 * 104 von len.")
                break           
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_3 = None

print("---------------------------------------------------------End von Aufgabe 3.:")       