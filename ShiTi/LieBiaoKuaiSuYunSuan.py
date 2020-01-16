from timeit import Timer

def func1():
    j = []
    for i in range(1000):
        j.append(i)


timeit1 = Timer("func1","from __main__ import func1")

print(f"{timeit1.timeit(1000)}")