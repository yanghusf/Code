a = [2,1,4,5,6,8]

def maopao(li):
    for i in range(len(li)):
        for j in range(len(li) -i):
            if a[j] > a[j+i]:
                a[j], a[j+1] = a[j+1], a[j]
    return li

a =maopao(a)
print(a)
