import sys, math, numpy, string
"""
        Task202
        Description: Write an algorithm to determine if a number n is happy.
                    A happy number is a number defined by the following process:
                    Starting with any positive integer, replace the number by the sum of the squares of its digits.
                    Repeat the process until the number equals 1 (where it will stay), or it loops endlessly in a cycle which does not include 1.
                    Those numbers for which this process ends in 1 are happy.
                    Return true if n is a happy number, and false if not.
        Constraints: 1 <= n <= 231 - 1
        Explanation:    Input: n = 19 Output: true                
                        1^2 + 9^2 = 82
                        8^2 + 2^2 = 68
                        6^2 + 8^2 = 100
                        1^2 + 0^2 + 0^2 = 1
        class Solution:
            def isHappy(self, n: int) -> bool:
                    
        Author:     RuslanLisovenko@gmail.com
        Date:       1608-2023        
"""

class Solution(object):

    # def __init__(self, iVarHappyNum: int, *arg, **kwarg):
    #     self.iHappyNum = int(iVarHappyNum)
    #     self.sUnParsingHappyNum = str(iVarHappyNum)        
    #     self.clsHappyResult = 0

    def methMagicWizard(self, iMagicNum) -> int:
        is_run, n = True , iMagicNum
        _sum_set = set()
        
        while True:            
            _sum = 0
            _n_str = str(n)
            for _ in _n_str:
                _sum += pow(int(_), 2)
            
            if _sum == 1:
                n = _sum
                break
            
            if _sum in _sum_set:
                n = _sum
                break

            _sum_set.add(_sum)
            n = _sum

        return n
    
    # def getMagicHappyNum(self) -> int:
    #     return self.clsHappyResult    

    def isHappy(self, n = 0):
        """
        :type n: int
        :rtype: bool
        """
    
        if self.methMagicWizard(n) == 1:
            return True
        else:
            return False

def main_test_202():    

    
    objSol = Solution()    

    input_01 = 19
    print(f'My Answer: {objSol.isHappy(input_01)} . Expected: True for Value:{input_01}')
    
    input_02 = 1
    print(f'My Answer: {objSol.isHappy(input_02)} . Expected: True for Value:{input_02}')

#------------------------------------------------------------
if __name__ == "__main__":
    
    #main_auto_125() #+main_cli()
    main_test_202()       
        

#class clsSolution_202(Solution):
#    pass

#------------------------------------------------------------------------------------------------
#if __name__ == "__main__":
#    try:
#        print("---------------------------------------------------------Start von Aufgabe 202. :")         
#        sInput = int(19)
#        clsObj_202 = clsSolution_202(sInput)        
#        print(f"Sie haben num:{sInput} und diese Num ist MagicHappyNum: ", clsObj_202.isHappyNum(19), " Result: ",clsObj_202.getMagicHappyNum())
#        print("---------------------------------------------------------End Test Aufgabe - > Write/schreiben Sie bitte stop fur end iteration.:")
#    except:
#        print("Sie haben eine Error:")
#    finally:
#        clsObj_169 = None

#print("---------------------------------------------------------End von Aufgabe 202. : ") 