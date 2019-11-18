import re
import lisp_namespace as ns

def isStr(atom):
    _string = "^([\"].*[\"])|([\'].*[\'])$"
    return re.match(_string, atom)

def isNum(atom):
    _number = "^[0-9]*\.?[0-9]*$"
    return re.match(_number, atom)

def isInt(atom):
    _int = "^[0-9]*$"
    return re.match(_int, atom)


def isKnownSymbol(atom):
    return atom in ns.symbols

def castString(atom):
    return atom[2:-2]

def cast(atom):
    if isStr(atom):
        return castString(atom)
    elif isInt(atom):
        return int(atom)
    elif isNum(atom):
        return float(atom)
    elif isKnownSymbol(atom):
        return ns.symbols[atom]
    else:
        return atom