"""
truple oder cortage
"""

my_truple = ()
my_truple = tuple(range(8))
print(my_truple)
myPersonTuple =("ves","rost","age")
print(myPersonTuple)

#unpack tuple
for index, value in enumerate(my_truple):
    print("values[{}] = {}".format(index, value))