import sys, math, numpy, string
"""
        Description: Given an array nums of size n, return the majority element. 
                     The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.  
        Constraints: n == nums.length1 <= n <= 5 * 104(50 000)
                     -109 <= nums[i] <= 109
                    
        Author:     RuslanLisovenko@gmail.com
        Date:       1608-2023        
"""
class Solution(object):       
    def __init__(self, CheckList: list):
        self.CheckList = list(CheckList)

    def methCheckConditions(self, CheckList: list) -> bool:
        """
            n == nums.length1 <= n <= 5 * 104
            -109 <= nums[i] <= 109
        """
        
        for iValue in CheckList:
            iLen = len(CheckList)
            iCount = CheckList.count(iValue)                 
            if  1 <= CheckList.count(iValue) and CheckList.count(iValue) <= 5*pow(10,4) \
                and len(str(iValue)) in range(-1 * pow(10,9), pow(10,9)) \
                and CheckList.count(iValue) <= len(CheckList):
                    #CheckList = list(set(CheckList).remove())                                        
                    continue
            else:                
                return False
            
        return True

    def getMaxMajorityElement(self, CheckList: list[int]):
        """
        :type nums: List[int]
        :rtype: int
        """
        self.CheckList = list(CheckList)
        sNewDict = {} #'key=value': 'CountValue'}
        iBegRange = -1*pow(10, 9)
        iEndRange = pow(10, 9)
        iFullRange = 5*pow(10, 4)

        #if self.methCheckConditions(CheckList) == True:            
            
        ListKey = 0
        CheckList = sorted(CheckList)
        sCheckList = "".join(str(elList) for  elList in CheckList)
        #sCheckList = sorted(sCheckList)

        while len(CheckList) > 0:
        
            for iIndexDict in range(len(CheckList)):                    
                
                if len(CheckList) == 0 : break                 
                    #Create  key(Value)->maxCount(als value) in List                   
                    #------------------------
                if  CheckList[iIndexDict] not in sNewDict.keys() :
                    
                    iKeyDisct =  CheckList[iIndexDict]                    
                    iCount = CheckList.count(iKeyDisct)
                    sNewDict.__setitem__(iKeyDisct, iCount)
                    #sCheckList = sCheckList.replace(iKeyDisctValue,"")                    
                    for i in range(iCount):CheckList.remove(iKeyDisct)
                    
                break

        bFlagRange = True        
    #---------------------------------Check range    
        for iValueKey  in sNewDict.keys():            
                      
            if iBegRange >= iValueKey or iValueKey <= iEndRange:
                continue                
            else:                
                bFlagRange = False
                break
    #---------------3 Step serch max count
        if bFlagRange is True:
            for iValueCount in sNewDict.values():
                #if _ValueCount in range(1, 5*pow(10, 4)):
                if 1 >= iValueCount or  iValueCount <= iFullRange:
                    continue                
                else:                
                    bFlagRange = False
                    break
        
        if  bFlagRange is True:
            
            ListKey = sorted(sNewDict,reverse = True)                         
            for iKeyDisct in ListKey : #range(len(sNewDict)):                
                if sNewDict[iKeyDisct] == max(sNewDict.values()) \
                    and iKeyDisct == max(sNewDict.keys()) :
                    return iKeyDisct #{_KeyDict: sNewDict[_KeyDict]}
                
                elif sNewDict[iKeyDisct] == max(sNewDict.values()) :
                    return iKeyDisct #{_KeyDict: sNewDict[_KeyDict]}        
        else:
            print("Out of range n == nums.length1 <= n <= 5 * 104 and -109 <= nums[i] <= 109" )
            return None
        return iKeyDisct    
   

#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 136. :") 
        
        sInput = [-1,1,1,1,2,1]         #list([4,1,2,1,2]) #[2,2,1,1,1,2,2]  antwort 2               
        clsObj_169 = Solution(sInput)        
        print(f"Sie haben list:{sInput} und diese Num ist Single: ",clsObj_169.getMaxMajorityElement(sInput))
        sInput = [8,8,7,7,7]
        print(f"Sie haben list:{sInput} und diese Num ist Single: ",clsObj_169.getMaxMajorityElement(sInput))
        sInput = [6,5,5]
        print(f"Sie haben list:{sInput} und diese Num ist Single: ",clsObj_169.getMaxMajorityElement(sInput))
        sInput = 50000 * [1,2, 3]
        print(f"Sie haben list: und diese Num ist Single: ->",clsObj_169.getMaxMajorityElement(sInput))
#-------------------------------
    
        sInput = 25000*[1] + 25000*[2]
        print(f"Sie haben list:{sInput} und diese Num ist Single: ->",clsObj_169.getMaxMajorityElement(sInput))
        print("---------------------------------------------------------End Test Aufgabe - > Write/schreiben Sie bitte stop fur end iteration.:")
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_169 = None

print("---------------------------------------------------------End von Aufgabe 136. : ") 