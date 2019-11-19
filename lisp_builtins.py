import lisp_environment as env

def eq(*args, **kwargs):
    _eq = True
    last = None
    for idx, item in enumerate(args):
        if idx == 0:
            last = item
        else:
            _eq = last == item
    return _eq


def add(*args, **kwargs):
    for idx, item in enumerate(args):
        if idx == 0:
            _sum = item
        else:
            _sum += item
    return _sum


def sub(*args, **kwargs):
    for idx, item in enumerate(args):
        if idx == 0:
            _diff = item
        else:
            _diff -= item
    return _diff


def mult(*args, **kwargs):
    for idx, item in enumerate(args):
        if idx == 0:
            _prod = item
        else:
            _prod *= item
    return _prod


def div(*args, **kwargs):
    for idx, item in enumerate(args):
        if idx == 0:
            _quot = item
        else:
            _quot /= item
    return _quot


def quote(*args, **kwargs):
    print(' '.join(str(arg) for arg in args))


def cons(*args, **kwargs):
    return tuple(args)


def car(*args, **kwargs):
    return args[0][0]


def cdr(*args, **kwargs):
    return args[0][1:]


def atom(*args, **kwargs):
    if len(args) > 1  or type(args[0]) == type(()):
        return False
    else:
        return True


def define(*args, **kwargs):
    ENV = kwargs['ENV']
    ENV.insert(args[0],args[1])
    return ENV.get(args[0])


def lambdef(*args, **kwargs):
    pass
    # params = args[0]
    # func = args[1]
    # print("params: ",params)
    # print('func: ',func)


def cond(*args, **kwargs):
    return args


def _return(*args, **kwargs):
    if len(args) > 1:
        args = list(args)
        args.insert(0, '(')
        args.append(')')
        quote(*args)
    else:
        print(*args)