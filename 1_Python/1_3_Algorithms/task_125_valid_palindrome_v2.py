"""
        Description: A phrase is a palindrome if, after converting all uppercase letters into lowercase letters and removing all non-alphanumeric characters, it reads the same forward and backward. Alphanumeric characters include letters and numbers.
                     Given a string s, return true if it is a palindrome, or false otherwise.
                     1 <= s.length <= 2 * 105
                     s consists only of printable ASCII characters.
                    
        Author:     RuslanLisovenko@gmail.com
        Date:       15.08.2023
"""

class Solution:
    
    from typing import Any

    def __init__(self):
        self.CortageNonIncludSymbol = ('', chr(32), '(', ')', '{', '}', '[', ']', '%', '#', ':', ';', '.', ',', '&', '@', '$', '?', '_')     #(0,1,2,3,4,5,6)
        self.clsResult = ""

    def getIsPalindromeResult(self):
        return self.clsResult

    def isPalindrome(self, sStr:str) -> bool:
        """
        :type s: str
        :rtype: bool
        """

        sStr = sStr.lower()
        for iIndex in range(len(self.CortageNonIncludSymbol)):
            sStr = sStr.replace(self.CortageNonIncludSymbol[iIndex], self.CortageNonIncludSymbol[0])

        self.clsResult = sStr[::-1]
        
        if sStr == self.clsResult:
            self.clsResult = sStr
            return True
        else:
            self.clsResult = sStr
            return False
        