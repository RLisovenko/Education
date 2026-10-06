import sys, math, numpy, string

"""
    Description file: Given two strings s and t, determine if they are isomorphic.
                        Two strings s and t are isomorphic if the characters in s can be replaced to get t.
                        All occurrences of a character must be replaced with another character while preserving the order of characters. No two characters may map to the same character, but a character may map to itself.
    Constraints:    1 <= s.length <= 5 * 104
                    t.length == s.length
                    s and t consist of any valid ascii character.

    Author:     RuslanLisovenko@gmail.com
    Date:       2208-2023
"""

class Solution(object):
    def isIsomorphic(self, str1: str, str2: str) -> bool:
        if len(str1) != len(str2):
            return False
        else:
            map1, map2 = {}, {}
            for i in range(len(str1)):
                ch1, ch2 = str1[i], str2[i]
                if ch1 not in map1:
                    map1[ch1] = ch2
                if ch2 not in map2:
                    map2[ch2] = ch1
                if map1[ch1] != ch2 or map2[ch2] != ch1:
                    return False
        return True
    
if __name__ == "__main__":
    sStr1 = "abacba"
    sStr2 = "xpxcpx"
    objSol = Solution()
    print(f'My Answer: {objSol.isIsomorphic(sStr1, sStr2)} . Expected: True for Value:{sStr1}  mapped {sStr2}')


