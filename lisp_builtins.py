import functools as func
import operator as op

def eq(*args, **kwargs):
    return func.reduce(op.eq, args)

def add(*args, **kwargs):
    return func.reduce(op.add,args)

def sub(*args, **kwargs):
    return func.reduce(op.sub,args)

def mult(*args, **kwargs):
    return func.reduce(op.mul,args)

def div(*args, **kwargs):
    return func.reduce(op.truediv,args)

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