import random
import time
#a = [43, 95, 47, 16, 100, 13, 88, 85, 56, 14]

a = []
start = time.perf_counter()
for i in range(30000):
    num = random.randint(0,10000000)
    a.append(num)
elapsed = (time.perf_counter() - start)
print('生成数组耗时：%f'%elapsed)

b = a

start = time.perf_counter()
b.sort()
elapsed = (time.perf_counter() - start)
print('系统排序耗时：%f'%elapsed)


#选择排序
def select(a):
    start = time.perf_counter()
    for i in range(len(a)):
        minn = i
        for j in range(i+1,len(a)):
            if a[minn] > a[j]:
                minn = j
        a[i], a[minn] = a[minn], a[i]
    elapsed = (time.perf_counter() - start)
    print('选择排序耗时：%f'%elapsed)
    return a
#冒泡排序
def bubble(a):
    start = time.perf_counter()
    for i in range(len(a)):
        isMove = False
        for j in range(0,len(a)-i-1):
            if a[j] > a[j+1]:
                a[j], a[j+1] = a[j+1], a[j]
                isMove = True
        if isMove==False: break
    elapsed = (time.perf_counter() - start)
    print('冒泡排序耗时：%f'%elapsed)
    return a
#插入排序
def insert(a):
    start = time.perf_counter()
    for i in range(1,len(a)):
        tmp = a[i]
        while a[i-1] > tmp and i>0:
            a[i] = a[i-1]
            i -= 1
        a[i] = tmp
    elapsed = (time.perf_counter() - start)
    print('插入排序耗时：%f'%elapsed)
    return a



print(insert(a)==b)
print(bubble(a)==b)
print(select(a)==b)






