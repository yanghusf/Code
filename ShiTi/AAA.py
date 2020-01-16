class A(object):
    def __init__(self, a, b):
        self.a1 = a
        self.b1 = b
        print('init')

    def mydefault(self, *args):
        print('default:' + str(args[0]))

    def __getattr__(self, name):
        print("other fn:", name)
        return self.mydefault


a1 = A(10, 20)
a1.fn1(33)
a1.fn2('hello')
a1.fn3(10)
