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


def quote(*args):
    print(' '.join(str(arg) for arg in args))


def cons(*args):
    return tuple(args)


def car(*args):
    return args[0][0]


def cdr(*args):
    return args[0][1:]


def atom(*args):
    if len(args) > 1  or type(args[0]) == type(()):
        return False
    else:
        return True


def define(*args):
    symbols[args[0]] = args[1]
    return symbols[args[0]]


def lambdef(*args):
    pass
    # params = args[0]
    # func = args[1]
    # print("params: ",params)
    # print('func: ',func)


def cond(*args):
    return args


def _return(*args):
    if len(args) > 1:
        args = list(args)
        args.insert(0, '(')
        args.append(')')
        quote(*args)
    else:
        print(*args)
            


functions = { 
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
    'cond': cond,
    '_return': _return
}


symbols = {
    'else': 'else'
}