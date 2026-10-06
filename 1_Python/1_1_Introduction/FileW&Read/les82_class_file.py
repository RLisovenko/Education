class myManageFile():
    def __init__(self):
        self.resource = 48
    def __enter__(self):
        print("Enter context")
        return self.resource
    def __exit__(self,exec_type,exec_value,exec_traceback):
        print("end context")
        if exec_type:
            print("exeption occured:{}".format(exec_type))

with    myManageFile() as resource:
    print("Some actions mit resource", resource)
    raise ValueError