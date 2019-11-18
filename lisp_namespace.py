def eq(*args):
    _eq = True
    last = None
    for idx, item in enumerate(args):
        if idx == 0:
            last = item
        else:
            _eq = last == item
    return _eq


def add(*args):
    for idx, item in enumerate(args):
        if idx == 0:
            _sum = item
        else:
            _sum += item
    return _sum


def sub(*args):
    for idx, item in enumerate(args):
        if idx == 0:
            _diff = item
        else:
            _diff -= item
    return _diff


def mult(*args):
    for idx, item in enumerate(args):
        if idx == 0:
            _prod = item
        else:
            _prod *= item
    return _prod


def div(*args):
    for idx, item in enumerate(args):
        if idx == 0:
            _quot = item
        else:
            _quot /= item
    return _quot


def quote():
    pass


def cons(*args):
    return tuple(args)


def car(*args):
    print("args: ",args)
    print("args[0]: ",args[0])
    return args[0][0]


def cdr(*args):
    print("args: ",args)
    print("args[0]: ",args[0])
    return args[0][1:]


def atom(*args):
    print('args: ',args)
    print('type(args[0]): ',type(args[0]))
    if len(args) > 1  or type(args[0]) == type(()):
        return False
    else:
        return True


def define(*args):
    symbols[args[0]] = args[1]
    return symbols[args[0]]


def lambdef(*args):
    pass


def cond(*args):
    pass

symbols = { 
    '+': add,
    '-': sub,
    '*': mult,
    '/': div,
    'eq?': eq,
    'quote': quote,
    'cons': cons,
    'car': car,
    'cdr': cdr,
    'atom?': atom,
    'def': define,
    'lambda': lambdef,
    'cond': cond
}