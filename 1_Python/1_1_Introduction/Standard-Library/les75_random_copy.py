"""
obj.deepcopy
obj.copy() копия из копии дает два одинаковіх обьектов после добавления
"""
import random

print("random.random", random.random())
print("random.randint",random.randint(1,1000))
print("random.sample", random.sample(range(100),10))
print("random.random", random.Random().random)
print("random.random", random.SystemRandom().random())