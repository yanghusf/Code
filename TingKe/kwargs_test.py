class A(object):
    def __init__(self, *args, **kwargs):
        self.name = args
        self.age = args
        self.k = kwargs


a = A("小明",12,job="it", sex=1)
print(a.name)
print(a.age)
print(a.k)