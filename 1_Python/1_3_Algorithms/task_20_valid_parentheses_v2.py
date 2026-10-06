import sys, math, numpy, string
from typing import Any
"""
        Description: Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
                        1 <= s.length <= 104
                        s consists of parentheses only '()[]{}'.      
        Author:     RuslanLisovenko@gmail.com
        Date:       1508-2023        
"""
class Solution:       
    def __init__(self):
        self.CortageOnlySymbol_const = ('(', ')', '{', '}', '[', ']')     #(0,1,2,3,4,5,6)
        self.distOnlySymbol_const = {"(": ')', '{': '}', '[': ']'}        #(key:value)
        self.distOnlySymbol_invert = {")": '(', '}': '{', ']': '['}        #(key:value)
        self.ErrSymbolReturn = ""
        """
        Python Dictionary clear()        Removes all Items
        Python Dictionary copy()         Returns Shallow Copy of a Dictionary
        Python Dictionary fromkeys()     Creates dictionary from given sequence
        Python Dictionary get()          Returns Value of The Key
        Python Dictionary items()        Returns view of dictionary (key, value) pair
        Python Dictionary keys()         Returns View Object of All Keys
        Python Dictionary pop()          Removes and returns element having given key
        Python Dictionary popitem()      Returns & Removes Element From Dictionary
        Python Dictionary setdefault()   Inserts Key With a Value if Key is not Present
        Python Dictionary update()       Updates the Dictionary als insert arbite
        Python Dictionary values()       Returns view of all values in dictionary
        """
    def getErrSymbolReturn(self):
        return self.ErrSymbolReturn
    
    def funcIsValid(self, sStr:str) -> bool:
        """
        :type s: str
        :rtype: bool
        """ 
        #print(f"sStr{iCurCount}",sStr[iCurCount])          
            #print(self.distOnlySymbol_const.keys())
            #print(self.distOnlySymbol_const.values())
            #print("value", self.distOnlySymbol_const.get(str(sStr[iCurCount]))) 
            #print("index",sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))))
            #ss = sStr[iCurCount : sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))) + 1]
            #print(ss)
            #        
        disctFlagColl = {} #"(": False, '{': False, '[': False}
        #-----------------------------------------------------------------------
        for iCurCount in range(len(sStr)):          
            #ss = self.distOnlySymbol_invert.get(sStr[iCurCount])

            #if  disctFlagColl.get("(") == True or  disctFlagColl.get('{') == True or  disctFlagColl.get('[') == True:
            #    break
            
            if sStr[iCurCount] in self.distOnlySymbol_const.keys() \
               and iCurCount <= sStr.find(self.distOnlySymbol_const.get(sStr[iCurCount])) \
               and sStr.count(sStr[iCurCount]) == sStr.count(self.distOnlySymbol_const.get(sStr[iCurCount])) \
               and iCurCount <= sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))) :

               if sStr[iCurCount] not in disctFlagColl.keys() or disctFlagColl[sStr[iCurCount]] == False : 
                   disctFlagColl.update({sStr[iCurCount] : True})
                   #disctFlagColl[sStr[iCurCount]] = True

                #continue

            elif  sStr[iCurCount] in self.distOnlySymbol_const.values() :
                if  self.distOnlySymbol_invert.get(sStr[iCurCount]) not in disctFlagColl.keys() \
                    and sStr.count(sStr[iCurCount]) != sStr.count(str(self.distOnlySymbol_invert.get(sStr[iCurCount]))) \
                    and    iCurCount > sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))):

                    disctFlagColl.update({self.distOnlySymbol_invert.get(sStr[iCurCount]) : False})

                elif self.distOnlySymbol_invert.get(sStr[iCurCount]) not in disctFlagColl.keys() \
                    and sStr.count(sStr[iCurCount]) == sStr.count(self.distOnlySymbol_invert.get(sStr[iCurCount])) \
                    and    iCurCount < sStr.find(str(self.distOnlySymbol_invert.get(str(sStr[iCurCount])))):

                    disctFlagColl.update({self.distOnlySymbol_invert.get(sStr[iCurCount]) : False})
                    break

                elif self.distOnlySymbol_invert.get(sStr[iCurCount]) not in disctFlagColl.keys() \
                    and sStr.count(sStr[iCurCount]) == sStr.count(self.distOnlySymbol_invert.get(sStr[iCurCount])):
                    
                    disctFlagColl.update({self.distOnlySymbol_invert.get(sStr[iCurCount]) : True})
                    
                else:
                    disctFlagColl[self.distOnlySymbol_invert.get(sStr[iCurCount])] = True
                                    
                #continue

            if  (sStr[iCurCount] in self.distOnlySymbol_const.values() and iCurCount == 0) \
                or  (sStr[iCurCount] in self.distOnlySymbol_const.values() and iCurCount == len(sStr) - 1 \
                and self.distOnlySymbol_invert.get(sStr[iCurCount]) not in sStr) \
                or (sStr[iCurCount] in self.distOnlySymbol_const.keys() and iCurCount == len(sStr) - 1) \
                or (sStr[iCurCount] in self.distOnlySymbol_const.keys() \
                and sStr.count(sStr[iCurCount]) != sStr.count(self.distOnlySymbol_const.get(sStr[iCurCount]))):                             

                disctFlagColl.update({sStr[iCurCount] : False})
                #disctFlagColl[self.distOnlySymbol_invert.get(sStr[iCurCount])] = False

                break

            elif sStr[iCurCount] in self.distOnlySymbol_const.keys() \
                 and sStr.count(sStr[iCurCount]) == sStr.count(self.distOnlySymbol_const.get(sStr[iCurCount])) \
                 and iCurCount <= sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))):
                
                disctFlagColl[sStr[iCurCount]] = True

                if self.distOnlySymbol_const.get(str(sStr[iCurCount])) == None:                
                    self.ErrSymbolReturn = str(sStr[iCurCount])
                    break   

                elif self.distOnlySymbol_const.get(str(sStr[iCurCount])) in sStr:                                    
                    iIndexBeg = iCurCount + 1 
                    iIndexEnd = (-1 * sStr[::-1].find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))) - 1)
                    iIndexEnd = len(sStr) + (-1 * sStr[::-1].find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))) - 1) 
                    
                    if iCurCount <= sStr.find(self.distOnlySymbol_const.get(str(sStr[iCurCount]))):
        #-----------------------------------------------------------------------                        
                        ss =  sStr[iIndexBeg : iIndexEnd] 
                        if len(ss) == 0:
                            if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): disctFlagColl[sStr[iCurCount]] =  True
                        else:                            
        #-----------------------------------------------------------------------
                        #if iCount: #if alle count paar return True
                        #else:
                            for iIndx in range(len(ss)):
                                if ss[iIndx] in self.distOnlySymbol_const.keys():
                                    if ss.count(ss[iIndx]) ==  ss.count(self.distOnlySymbol_const.get(ss[iIndx])):
                                        if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): 
                                            disctFlagColl[sStr[iCurCount]] = True
                                            break
                                    else:
                                        if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): 
                                            disctFlagColl[sStr[iCurCount]] = False
                                            #return False
                                elif ss[iIndx] in self.distOnlySymbol_const.values():
                                        if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): disctFlagColl[sStr[iCurCount]] = False
                                        return False
                                else:
                                    if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): 
                                        disctFlagColl[sStr[iCurCount]] = True
                                        #if ss[iIndx] in self.distOnlySymbol_const.keys():
                                        #    if self.distOnlySymbol_const.get(ss[iIndx]) in ss \
                                        #        and iIndx < ss.find(self.distOnlySymbol_const.get(ss[iIndx])):                                    
                                        #        bFlag = True
                                        #    else:
                                        #        bFlag = False                                            
                                        #elif ss[iIndx] in self.distOnlySymbol_const.values():
                                        #    bFlag = False                                             
                                        #else:   
                                        #    bFlag = True
                    else: 
                        if disctFlagColl[sStr[iCurCount]] not in disctFlagColl.keys(): disctFlagColl[sStr[iCurCount]] = False
                else:
                    self.ErrSymbolReturn = str(sStr[iCurCount])
                    break
            

        if  disctFlagColl.get("(") == False \
            or  disctFlagColl.get('{') == False \
            or  disctFlagColl.get('[') == False:
                return False                   
        else:   return True
        

#------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 20. :") 
        clsObj_20 = Solution()
        print("TRue",clsObj_20.funcIsValid("(([]){})"))
        print("False",clsObj_20.funcIsValid("]["))
        print("False",clsObj_20.funcIsValid("[([]])"))
        print("False",clsObj_20.funcIsValid("([]"))
        print("False",clsObj_20.funcIsValid("[])"))

        print("True",clsObj_20.funcIsValid("()"))
        print("True",clsObj_20.funcIsValid("(([]){})"))
        print("True",clsObj_20.funcIsValid("{[]}"))
        print("False",clsObj_20.funcIsValid("[([]])"))
        print("False",clsObj_20.funcIsValid("[])"))
        
        print("False",clsObj_20.funcIsValid(")(){}"))
        print("False",clsObj_20.funcIsValid("({{{{}}}))"))
        print("False",clsObj_20.funcIsValid("(){}}{"))
              
        print("True",clsObj_20.funcIsValid("()[]{}"))
        print("False", clsObj_20.funcIsValid("([)]"))
        print("True", clsObj_20.funcIsValid("{[]}"))
        sStr = ""
        while sStr != 'stop':
            sStr = str(input("Input fur ()[]{} correct verglechen : "))
            if len(sStr) > 0 and len(sStr) <= 104:
                bStrVergleichValue = clsObj_20.funcIsValid(sStr)
                print(" Test str von ()[]{} : ", bStrVergleichValue)
                if bStrVergleichValue == False: print(f"Erorr mit symbol {clsObj_20.getErrSymbolReturn()}.\n Sie muss open und close benutzen.") 
                print("---------------------------------------------------------while - > Write/schreiben Sie bitte stop fur end iteration.:")
            else:
                print("Enter bitte sStr correct ()[]{}.")
                break       
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_20 = None

print("---------------------------------------------------------End von Aufgabe 20. : ")       