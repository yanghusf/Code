from typing import List, Tuple,overload

@overload
def foo(name: str)-> str:
    return "hello" + name

@overload
def foo(name: int)-> str:
    return "hello" + str(name)


def foo(name):
    return "hello" + str(name)

# a =foo(2.0)
# print(a)
from typing import Union, Tuple, List, S

def converter(i: str, node: str) -> Tuple[str, bool]:
    return "abc",True

# a = converter("abc", "11")
# print(a)

def func(a:int, string:str) -> List[int or str]:
    print()
