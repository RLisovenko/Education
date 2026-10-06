
class cls_Erorr(BaseException):
    """
try: # область действия обработчика
…
except Exception1: # обработчик исключения Exception1
…
except Exception2: # обработчик исключения Exception2
…
except: # стандартный обработчик исключений
…
else: # код, который выполняется, если никакое
… # исключение не возникло
finally: # код, который выполняется в любом случае
----------------------------------------------------
SyntaxError
eval или exec. запускает любой код
----------------------------------------------------
BaseException Базовый класс для всех исключений.
Exception   - всех стандартных исключений
ArithmeticError связанных с арифметическими операциями.
Warning  - базовым классом для предупреждений от Exception
UserWarning. =- warn (message).

    """
    def __init__(self, myError = ""):
        self.cls_error = myError
    def __del__(self):
        pass
    def func_prn_Error(self, objErr = ValueError ):
        self.cls_error = objErr
        try:
            print("1-try: Arrea arbeit ", self.cls_error)
        except (ValueError, TypeError) as variableError:
            print("except", objErr)
        except :
            print(objErr)
        else:
            print("2-else any except nicht werden", self.cls_error)
            #if neimand except nict werden
        finally:
            print("3- finally: Kod run в любом случае",self.cls_error)
            # zunbeischpiel del exemlyar class __del__(self)


myObjErr = cls_Erorr()
myObjErr.func_prn_Error()