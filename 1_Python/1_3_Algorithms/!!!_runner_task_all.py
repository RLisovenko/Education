#-------------------------------------------------------------------------------------------------------------------------
"""
    Aufgaben nach dem Audit:
    Author: RuslanLisovenko
    Date:   1011-2023
    refrech 26.10.2025
"""
#-------------------------------------------------------------------------------------------------------------------------
def task_9_palindrome():
    from task_9_palindrome import Solution

    input_01 = -121
    objSol = Solution(input_01)    
    print(f'My Answer: {objSol.IsPalindrome(input_01)} . Expected: True for False:{input_01}')
    input_01 = 121
    objSol = Solution(input_01)    
    print(f'My Answer: {objSol.IsPalindrome(input_01)} . Expected: True for Value:{input_01}')
#-------------------------------------------------------------------------------------------------------------------------
def task_7_reverse():
    from task_7_reverse import Solution

    input_01 = 777 #enteer deine nummer
    objSol = Solution()
    print(f'My Answer: {objSol.reverse(input_01)} . Expected: True\False for Value:{input_01}')
#-------------------------------------------------------------------------------------------------------------------------
def task_869_pow_2():
    from task_869_pow_2_v1008_23 import Solution

    input_01 = 10
    objSol = Solution(input_01)    
    print(f'My Answer: {objSol.funcReorderedPowerOf2(input_01)} . Expected: False for Value:{input_01}')

    input_01 = 46    
    print(f'My Answer: {objSol.funcReorderedPowerOf2(input_01)} . Expected: True for Value:{input_01}')

    input_01 = 218    
    print(f'My Answer: {objSol.funcReorderedPowerOf2(input_01)} . Expected: True for Value:{input_01}')
#-------------------------------------------------------------------------------------------------------------------------
def task_383_ransom_note():
    from task_383_ransom_note import Solution

    strSearchText = "aab"
    strAllText = "baa"
    objSol = Solution(strSearchText,strAllText)    
    print(f'My Answer: {objSol.funcSearchTextInText(strSearchText, strAllText)} . Expected: True for Value:{strSearchText}')

    strSearchText = "fffbfg"
    strAllText = "effjfggbffjdgbjjhhdegh"  
    print(f'My Answer: {objSol.funcSearchTextInText(strSearchText, strAllText)} . Expected: True for Value:{strSearchText}')

    strSearchText = "aab"
    strAllText = "aablklk"   
    print(f'My Answer: {objSol.funcSearchTextInText(strSearchText, strAllText)} . Expected: True for Value:{strSearchText}')

#-------------------------------------------------------------------------------------------------------------------------
def task_168_exl_num_to_symbol():
    from task_168_exl_num_to_symbol_v5_08112023 import Solution

    iNumCol = 1
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")
    iNumCol = 26
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")

    iNumCol = 701
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")
    iNumCol = 702
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")
    
    iNumCol = 1403
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")
    iNumCol = 1404
    obj = Solution()
    print(f"Column {iNumCol}: ->to char-> {obj.convertToTitle(iNumCol)}")
#-------------------------------------------------------------------------------------------------------------------------
def task_326_power_3():
    from task_326_power_3 import Solution

    
    obj = Solution()
    iNumPow_n = 3
    print(f"Value {iNumPow_n}: ->to -> {obj.isPowerOfThree(iNumPow_n)}")    
    iNumPow_n = 27    
    print(f"Value {iNumPow_n}: ->to -> {obj.isPowerOfThree(iNumPow_n)}")    
    iNumPow_n = 100
    print(f"Value {iNumPow_n}: ->to -> {obj.isPowerOfThree(iNumPow_n)}")
#-------------------------------------------------------------------------------------------------------------------------
def task_13_roman_to_int():
    from task_13_roman_to_int import Solution
    
    obj = Solution()
    print("---------------------------------------------------------Parsing Roman to int .:")
    print("value I:  ", obj.romanToInt('I')) 
    print("value V:  ", obj.romanToInt('V')) 
    print("value X:  ", obj.romanToInt('X'))        
    print("Value L:  ", obj.romanToInt('L'))
    print("Value C:  ", obj.romanToInt('C'))
    print("Value D:  ", obj.romanToInt('D'))
    print("Value M:  ", obj.romanToInt('M'))  

    sRomanNum = 'CXI' #111
    print(f"Value {sRomanNum}: ->to -> {obj.romanToInt(sRomanNum)}")   
    sRomanNum = 'MMCCLV' #2255
    print(f"Value {sRomanNum}: ->to -> {obj.romanToInt(sRomanNum)}")   
#-------------------------------------------------------------------------------------------------------------------------
def task_3_longest_sub_string():
    from task_3_longest_sub_string import Solution
    
    obj = Solution()
    vValue = "aaca"
    print(f"Value {vValue}: ->antwort -> abba 2 len -> {obj.funcGetLengthOfLongestSubStringOhneRepeatChar(vValue)}")   
    vValue = "cdd"
    print(f"Value {vValue}: ->antwort -> cdd len 1 -> {obj.funcGetLengthOfLongestSubStringOhneRepeatChar(vValue)}") 
    vValue = "bbbbb"
    print(f"Value {vValue}: ->antwort -> bbbbb len 1-> {obj.funcGetLengthOfLongestSubStringOhneRepeatChar(vValue)}") 
    vValue = "pwwkew"
    print(f"Value {vValue}: ->antwort -> antwort -> wke len 3-> {obj.funcGetLengthOfLongestSubStringOhneRepeatChar(vValue)}") 
    vValue = "abcabcbb"
    print(f"Value {vValue}: ->antwort -> antwort -> abcabcbb len 3-> {obj.funcGetLengthOfLongestSubStringOhneRepeatChar(vValue)}") 
#-------------------------------------------------------------------------------------------------------------------------
def task_20_valid_parentheses_v2():
    from task_20_valid_parentheses_v2 import Solution
    
    obj = Solution()
    print("TRue",obj.funcIsValid("(([]){})"))
    print("False",obj.funcIsValid("]["))
    print("False",obj.funcIsValid("[([]])"))
    print("False",obj.funcIsValid("([]"))
    print("False",obj.funcIsValid("[])"))
    print("True",obj.funcIsValid("()"))
    print("True",obj.funcIsValid("(([]){})"))
    print("True",obj.funcIsValid("{[]}"))

#-------------------------------------------------------------------------------------------------------------------------
def task_434_number_segments_in_str():
    from task_434_number_segments_in_str import Solution
    
    obj = Solution()    
    sInput = "    Of all the gin joints in all the towns in all the world,   "
    print("Sie haben segment: ",obj.funcCountSegments(sInput))
#-------------------------------------------------------------------------------------------------------------------------
def task_125_valid_palindrome_v2():
    from task_125_valid_palindrome_v2 import Solution
    
    obj = Solution()    
    sInput = "A man, a plan, a canal: Panama"
    print(f"Sie haben {sInput} is a palindrome segment: ",obj.isPalindrome(sInput))
    sInput = "race a car"
    print(f"Sie haben {sInput} is not a palindrome segment: ",obj.isPalindrome(sInput))

#-------------------------------------------------------------------------------------------------------------------------
def task_136_arr_single_number():
    from task_136_arr_single_number import Solution
    
    obj = Solution([1])    
    sInput = list([4,1,2,1,2])  
    print(f"Sie haben {sInput} is antwort 4: ",obj.getSingleNumberOhneDuplicate(sInput))
    sInput = list([2,2,1])  
    print(f"Sie haben {sInput} is antwort 1: ",obj.getSingleNumberOhneDuplicate(sInput))

#-------------------------------------------------------------------------------------------------------------------------
def task_169_majority_el():
    from task_169_majority_el import Solution
    
    obj = Solution([-1,1,1,1,2,1])  #egal vvogu  ne imeet znachenia
    sInput = [-1,1,1,1,2,1]
    print(f"Sie haben list:{sInput} und diese Num ist Single: ", obj.getMaxMajorityElement(sInput))  

    sInput = [8,8,7,7,7]
    print(f"Sie haben list:{sInput} und diese Num ist Single: ", obj.getMaxMajorityElement(sInput))

    sInput = [6,5,5]
    print(f"Sie haben list:{sInput} und diese Num ist Single: ", obj.getMaxMajorityElement(sInput))    

    sInput = 50000 * [1,2, 3]
    obj = Solution([-1,1,1,1,2,1])    
    print(f"Sie haben list: und diese Num ist Single: ->", obj.getMaxMajorityElement(sInput))    

    # Ne pomnu kakoito variant optimizirovan 
    #sInput = 25000*[1] + 25000*[2] 
    #print(f"Sie haben list:{sInput} und diese Num ist Single: ->",obj.getMaxMajorityElement(sInput))
#-------------------------------------------------------------------------------------------------------------------------
def task_202_happy_number():
    from task_202_happy_number import Solution
    
    obj = Solution()    #egal vvogu  ne imeet znachenia
    input_01 = 19
    print(f'My Answer: {obj.isHappy(input_01)} . Expected: True for Value:{input_01}')
    
    input_02 = 1
    print(f'My Answer: {obj.isHappy(input_02)} . Expected: True for Value:{input_02}') 
#-------------------------------------------------------------------------------------------------------------------------
def task_205_isomorphic_strings():
    from task_205_isomorphic_strings import Solution
    
    obj = Solution()
    sStr1 = "abacba"
    sStr2 = "xpxcpx"    
    print(f'My Answer: {obj.isIsomorphic(sStr1, sStr2)} . Expected: True for Value:{sStr1}  mapped {sStr2}')

#------------------------------------------------------------

if __name__ == "__main__":

    while True:
        
        print(7*"*******Begin")        
        iTaskNummer = input("Enter bitte nur numer von Aufgabe\Task nur als integer oder 0 als exit: ").lower()
        match iTaskNummer:
            case 'exit':
                break
            case '0':
                break
            case '9':
                task_9_palindrome()
            case '7':
                task_7_reverse()
            case '869':
                task_869_pow_2()
            case '383':
                task_383_ransom_note()
            case '168':
                task_168_exl_num_to_symbol()
            case '326':
                task_326_power_3()
            case '13':
                task_13_roman_to_int()
            case '3':
                task_3_longest_sub_string() # ne sdal ne dodelal
            case '20':
                task_20_valid_parentheses_v2() #nicht gemaht
            case '434':
                task_434_number_segments_in_str()
            case '125':
                task_125_valid_palindrome_v2()
            case '136':
                task_136_arr_single_number()
            case '169':
                task_169_majority_el()
            case '202': #
                task_202_happy_number()
            case '205': #pomoemu etu balovalsia s etim map1, map2 = {}, {} и наткнулся на решение, не помню уже
                task_205_isomorphic_strings()                     
            #case _ :
            #    print("Habe nicht dieser Nummer von Aufgabe. enter bitte andere Numer.")
        print(f"---------------End---->TaskNummer = ",iTaskNummer)

    

#----------------------------------------Altere description von Augabe_1 ab Aug/Sep 2023      
    #main_auto_125() #accept +main_cli()
    # task _7 accept
    #main_test_202()#accept
    #main_test_9()#accept
    #main_test_869()#accept
    #main_test_125() #accept
    #main_test_326() # accept yslovia do ne vernu -3 not in range(-pow(3,1)) 
    #main_test_13() # accept # roman strannii 2216->"MCMXCIV"-> 1994 y minia - >MDCCCCLXXXXIIII
    #main_test_136() #accept
    
    #434 acccept
    #main_test_169()  -- ACCEPRT Eischeidung del element out of time Time Limit Exceeded -> "Out of range n == nums.length1 <= n <= 5 * 104 and -109 <= nums[i] <= 109" 
    #383 -- accept
#-----------------------------------------------------------------------------
    
    #3
    #20
    #168 - Excel

    #-----------------------------------------------------