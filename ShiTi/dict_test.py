import json
class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getitem__(self, item):
        return


sa = Student("XiaoMing",10)
print(json.dumps(sa,default=lambda x:x.__dict__))