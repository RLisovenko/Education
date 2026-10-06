import array
import os
#--------------------------------open file fu[r read und an  bild sehen

myfile = os.path.join('data','fileNumBin.bin')
myfileSize = os.path.getsize(myfile)
print(myfileSize)
print(array.array('i').itemsize)
myFileBlockCount = myfileSize // array.array('i').itemsize
print(myFileBlockCount)
#создаем массив длиной файла и fill заполняем нулями
myArr_numbers = array.array('i', (0 for _ in range(myFileBlockCount)))
print(myArr_numbers)

with open(myfile,"rb") as bin_file:
    try:
        #read data aus bin_file into array
        bin_file.readinto(myArr_numbers)
        print("myArr_numbers als array",myArr_numbers)
        print("myArr_numbers.tolist als list", myArr_numbers.tolist())
    except:
        print("present except")
    finally:
        print("bin_file.close")
        bin_file.close()
    print("---------",myArr_numbers.tolist())

    iCountNum = 1
    for myArrNum in myArr_numbers:
        print(f'myArrNum for {iCountNum}: ',myArrNum)
        iCountNum += 1
