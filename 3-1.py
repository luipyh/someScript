import random

c = 0
nc = 0
a = 1000000

for i in range(a):
    j = random.randint(1,3)
    s = random.randint(1,3)
    if s != j:
        c += 1
    if s == j:
        nc += 1
print(c/a)
print(nc/a)
    
    
