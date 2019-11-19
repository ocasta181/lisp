import re
import lisp_builtins as _globals
import lisp_environment as env

def isStr(atom):
    _string = "^([\"].*[\"])|([\'].*[\'])$"
    return re.match(_string, atom)

def isNum(atom):
    _number = "^[0-9]*\.?[0-9]*$"
    return re.match(_number, atom)

def isInt(atom):
    _int = "^[0-9]*$"
    return re.match(_int, atom)

def isKnownSymbol(atom, ENV):
    return ENV.find(atom)

def castString(atom):
    return atom[2:-2]

def cast(atom, ENV):
    if isStr(atom):
        return castString(atom)
    elif isInt(atom):
        return int(atom)
    elif isNum(atom):
        return float(atom)
    else:
        scope = isKnownSymbol(atom, ENV)
        if scope:
            return scope.get(atom)
        else:
            return atom