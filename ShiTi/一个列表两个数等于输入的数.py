def sum2(list,target):
    for i, j in enumerate(list):
        num1 = target-j
        if num1 in list:
            if list.index(num1) == i:
                print(num1,list.index(num1))


a = [1, 3, 4, 6, -3, 4, 1, 3, 8, 9, 3, 0, -3, 6, 0, 2, 9]
sum2(a, 6)

filter()
map()
