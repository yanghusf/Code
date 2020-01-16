def aa():
    print('hh')
    yield '1'
    print('gg')
    yield '2'
    print('ff')
    yield '3'

c = aa()

d = ''.join(c)
print(d)