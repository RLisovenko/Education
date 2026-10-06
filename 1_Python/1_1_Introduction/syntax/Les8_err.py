"""
Operator обратботка ошибок
NameError
TypeError
ValueError
AccerptionError -вираз в функціі є хибний
Importerorr
"""
def  MyExceptionErr(objMyException):
    """"
    My class  exception
    """
    try:
        objObj=None
    except ValueError:
        objObj = objException
        print("Bad ValueError: ", type(objException))
    except IndexError:
        objObj = objException
        print("Bad Index: ", type(objObj))
    except  Exception:
        # лучше не исп перехватівает нижние собітия или до нео описывать
        oObj = objException
        print("Bad Andere err: ", type(objObj))
    return type(objObj)
    #pass

def fFetCher(oObj: object,iIndex: int):
    return oObj[iIndex]

if __name__ == "__main__":
    try:
        objObj = str(input("Input objString bitte: "))
        print(f"prn len obj: {len(objObj)}")
        indMyIndex = input("Input index bitte: ")
        if indMyIndex < len(objObj) and len(objObj) > 0:
            print(f" pos {indMyIndex} ein:  {fFetCher(objObj, indMyIndex)} -> return LenObj: {len(objObj)}")
        elif indMyIndex == len(objObj):
            print("Dieses obj[0,1,2,3,4....] habe index = (len-1=): ",indMyIndex-1)

        elif len(objObj) == 0:
            print("Object habe nicht len")
        elif type(objObj) != str or type(indMyIndex) != int :
            raise TypeError
        else:
            raise ValueError
            #print("Problem mit obj zur lange oder andere")
    except  ValueError:
            print(f"ValueError: Bad index {indMyIndex} fur Obj: {objObj}")
    except  TypeError:
        print(f"TypeError: Bad  {type(objObj)} -->obj: {objObj}" )
    #except  Exception :
    #        print("MyExceptionErr", MyExceptionErr(Exception))



#----------------run section
#oObj="qwerty"
#iIndex = int(input("Input index bitte: "))
#print("return obj:  ",fFetCher(oObj,iIndex))

#--assert len(objObj) > 22 , "Zur lange obj"
            #print(" -> return LenObj: ",len(objObj))
            #raise ValueError
            # генерируем сами ошибку
            #print(f"return obj:  {fFetCher(objObj, indMyIndex)} -> return LenObj: {len(objObj)}")