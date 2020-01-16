def add(n,i):
    print(f"add--n:{n},i:{i}")
    return n +i

def test():
    for i in range(4):
        yield i
g = test()

for n in [1,10,5]:

    g = (add(n,i) for i in g)
    # g = (add(n, 2) for i in g)
# print()
print(list(g))