@Function
def sq(*args):
    num, *_ = args
    return num * num

root = Function(lambda *args: args[0]**.5)

@Function
def twice(*args):
    num, *_ = args
    return num * 2

@Function
def thrice(*args):
    num, *_ = args
    return num * 3

@Function
def add(a, b=0):
    return a + b

@Function
def mul(a, b=1):
    return a * b

@Function
def pow(a, b=1):
    return a ** b
