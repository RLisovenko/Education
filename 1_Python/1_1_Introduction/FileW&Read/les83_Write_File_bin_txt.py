import array
import random
import os


#----------------------------формирование

myNumArr = [random.randint(-10**6, 10**6)
            for _ in range(1000)]

#open txt file
with open(os.path.join('data','fileNumTxt.txt'),"w") as text_file:
    try:
        for myNum in myNumArr:
            text_file.write("{}\n".format(myNum))
        num_Arr = array.array("i",myNumArr)
    finally:
        text_file.close()

#open bin file
with open(os.path.join('data','fileNumBin.bin'),"wb") as bin_file:
    try:
        bin_file.write(num_Arr)
    finally:
        bin_file.close()

myNumArr = num_Arr = None

#--------------------------------open file fu[r read und an  bild sehen
with open(os.path.join('data','fileNumTxt.txt'),"r") as text_file:
    print("start myNumArr", myNumArr)
    try:
        # numbers = [int(line) for line in txt_file]
        #oder
        for line in text_file:

            myNumArr = [int(line)]
            print("nach myNumArr", myNumArr)
            print("line:", myNumArr)
    except:
        print("present error except")
        pass
    finally:
        text_file.close()

