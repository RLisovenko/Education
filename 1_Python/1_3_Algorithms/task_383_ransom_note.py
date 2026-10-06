import sys, math, numpy, string
from uu import Error

"""
    Description 383:
                Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.
                Each letter in magazine can only be used once in ransomNote.
    Constraints: 1 <= ransomNote.length, magazine.length <= 105
                ransomNote and magazine consist of lowercase English letters.
    Author:     RuslanLisovenko@gmail.com
    Date:       1008-2023
"""
class Solution():
    def __init__(self, strSearchText: str, strAllText: str):
            self.strSearchText = strSearchText.lower()
            self.strAllText = strAllText.lower()

    def funcSearchTextInText(self, strSearchText: str, strAllText: str) -> bool:

        if 1 <= len(self.strSearchText) and len(self.strAllText) <= pow(10,5):
            #somestring.contains("blah")
            strSearchText = strSearchText.lower()
            strAllText = strAllText.lower()
            sStrInvert = strSearchText[::-1].lower()
            sNewStr = ""
            iLenStartAll = len(strAllText)
            #strAllText = ", ".join(list(sElement), for sElement in strAllText)

            if  strSearchText in strAllText or \
                sStrInvert in strAllText: 
            #if  strAllText.find(strSearchText) != -1 or strAllText.find(sStrInvert) != -1: 
                #if stimt in string
                return True
            else:  
                for ii in range(len(strSearchText)):
                    if strSearchText[ii] in strAllText:                        
                        sNewStr = sNewStr + strSearchText[ii]                        
                        strAllText = strAllText.replace(strSearchText[ii],"",1)                        
                    else:
                        return False 
                if sNewStr == strSearchText: return True
        else: 
            return False
             
#--------------------------------------------    
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 383.:")
        #strSearchText = str(input("enter bitte String SearchText fur search in range  1 <= ransomNote.length: "))
        #strAllText = str(input("enter bitte String in Welhem Text Search fur search in range magazine.length <= 105: "))

        #strSearchText = "qweRty"
        #strAllText = "QwertyQwertz"
        #strSearchText = "bdjijj"
        #strAllText = "aifbigejbibiefgeffhabgeejdbiajgaahjefhdegafhfcigjaecbfiechadiehhfcejhhfbbdjheecfaijdba"
        #strSearchText = "aaa"
        #strAllText = "aba"
        strSearchText = "fihjjjjei"
        strAllText = "hjibagacbhadfaefdjaeaebgi"
        clsObj_383 = Solution(strSearchText, strAllText)
        boolResult  = clsObj_383.funcSearchTextInText(strSearchText, strAllText) 
        print(f"Das string {strSearchText} in lowcase {strAllText} {boolResult} eingangen, der Result ist : ",boolResult)

        if len(strSearchText) >= 1 and len(strAllText) <= 105:
            clsObj_383 = Solution(strSearchText, strAllText)
            boolResult  = clsObj_383.funcSearchTextInText()        
            if boolResult == True:
                print(f"Das string {strSearchText} in lowcase {strAllText} {boolResult} eingangen, der Result ist : ",boolResult)
            else:
                print(f"Das string {strSearchText} in lowcase {strAllText} {boolResult} eingangen, der Result ist : ",boolResult)
        else:
             print("Out von Kriterien. Input bitte correctly DATA.")
    except:
         print("Sie haben eine Error:", Error)
    finally:
         clsObj_383 = strSearchText = strAllText = None
