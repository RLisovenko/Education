import sys, math, numpy, string
"""
        Description: Given a non-empty array of integers nums, every element appears twice except for one. Find that single one.
                     You must implement a solution with a linear runtime complexity and use only constant extra space.
                        1 <= nums.length <= 3 * 104
                        -3 * 104 <= nums[i] <= 3 * 104
                        ach element in the array appears twice except for one element which appears only once.  
                    
        Author:     RuslanLisovenko@gmail.com
        Date:       1608-2023        
"""
class Solution:       
    def __init__(self, CheckList: list):
        self.CheckList = list(CheckList)

    def getSingleNumberOhneDuplicate(self, iNums: list[int]) -> int:
        """
        :type nums: List[int]
        :rtype: int
        """
        self.CheckList = iNums
        if self.methCheckConditions() == True:
            for iIndex in range(len(self.CheckList)):                       
                if self.CheckList.count(self.CheckList[iIndex]) == 1: #finden vor ersten Single num
                    return self.CheckList[iIndex]
                    #break
                else:
                    continue
        else:
            print("Out of Range: /n 1 <= nums.length <= 3 * 104 /n -3 * 104 <= nums[i] <= 3 * 104")
            return None

    def methCheckConditions(self) -> bool:
        """
            1 <= nums.length <= 3 * 104
            -3 * 104 <= nums[i] <= 3 * 104
        """
        
        for iValue in self.CheckList:
            if 1 <= len(str(iValue)) and len(str(iValue)) <= 3*pow(10,4):
                if -3 * pow(10,4) <= iValue and iValue <= 3 * pow(10,4):
                    continue
                else:
                    return False                
            else:                
                return False
        return True
                 
                
#------------------------------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        print("---------------------------------------------------------Start von Aufgabe 136. :")         
        sInput = list([4,1,2,1,2])        
        clsObj_136 = Solution(sInput)        
        print(f"Sie haben list:{sInput} und diese Num ist Single: ",clsObj_136.getSingleNumberOhneDuplicate(sInput))
        print("---------------------------------------------------------End Test Aufgabe - > Write/schreiben Sie bitte stop fur end iteration.:")
    except:
        print("Sie haben eine Error:")
    finally:
        clsObj_136 = None

print("---------------------------------------------------------End von Aufgabe 136. : ") 