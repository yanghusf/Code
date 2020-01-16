class Bar:
    def __init__(self, p1):
        self.p1 = p1

    def __call__(self, func):
        def wrapper():
            print("Staring", func.__name__)
            print("p1", self.p1)
            func()
            print("Ending", func.__name__)
        return wrapper

@Bar("foo bar")
def hello():
    print("Hello")

hello()