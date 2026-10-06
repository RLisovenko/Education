
class Solution:
    
    def reverse(self, x: int) -> int:
        import math
        result = 0
        _x = str(x)
        
        if x > 0:
            result = _x[::-1]
        else:
            result = '-' + str(abs(x))[::-1]
        
        result = int(result)
        _pow = math.pow(2, 31)
        if (result >= (-1 * _pow)) and (result < _pow - 1):            
            result = int(result)
        else:
            result = 0
        
        return result

#------------------------------------------
sol = Solution()
print(sol.reverse(123))
