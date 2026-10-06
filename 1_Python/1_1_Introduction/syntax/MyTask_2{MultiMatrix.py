"""
use Метод Функции Map()
MultiplyMultiArray
MyArrayMultiLevel = [1,[2,23,24,25],3,[41,42,43,44],6,7,8,9]
print(MyArrayMultiLevel[0])
print(MyArrayMultiLevel[1:0])
урок 5 1ю.50
"""

MyArrayMultiLevel_1 = [[11,12,13,14],[21,22,23,24],[31,32,33,34],[41,42,43,44]]
MyArrayMultiLevel_2 = MyArrayMultiLevel_1[::-1]
print("----------------ersten MyArray")
print(MyArrayMultiLevel_1)
iRowArray = 0
MyArrayResult = []
for MyArray_1_Rows in MyArrayMultiLevel_1:
    #print(f"Print MyArray_1_Rows: {MyArray_1_Rows}")
    # nehmen rows
    iColArray = 0
    print(f"--------andere Row {iRowArray}")
    #iRowArray = 0
    #MyArrayResult.append(MyArray_1_Rows)    # одной строкой или текст внизу oder ---------------
    for MyArray_1_el_Row in MyArray_1_Rows:
        iRes_1 = int(MyArray_1_el_Row)
        iRes_2 = int(MyArray_1_el_Row)
        #MyArrayResult[iRowArray:iColArray] = [iRes_1*iRes_1]
        MyArrayResult.append(iRes_1 * iRes_1)
        print(f"--element({iRowArray} : {iColArray}) = {MyArray_1_el_Row} in RowMyArray): {MyArray_1_Rows}")
        iColArray += 1

    iRowArray += 1

print("----------MyArrayResult--------")
print(MyArrayResult)
print(MyArrayResult[0])
#print(MyArrayResult[1])
#print(MyArrayResult[2])
#print(MyArrayResult[3])