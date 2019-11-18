#!/usr/bin/env python3

import sys, re
from collections import deque
import lisp_namespace as ns
import lisp_types as types

# # Postfix Lisp

def tolkenize(char):
    global stack
    global buffer
    global atombuffer
    global isString
    global isList
    if isString:
        atombuffer += char
        if char == isString:
            isString = False
            if atombuffer: 
                buffer.append(atombuffer[::-1])
            atombuffer = ''
    else:
        if char == '"' or char == "'":
            isString = char
            atombuffer += char
        elif char == ')':
            isList = True
            stack.append(buffer)
            buffer = []
            atombuffer = ''
        elif char == '(':
            if atombuffer:
                buffer.append(types.cast(atombuffer[::-1])) 
            last = stack.pop()
            last.append(parse(buffer))
            buffer = last
            atombuffer = ''
            isList = False
        elif char == ' ':
            if atombuffer:
                atom = types.cast(atombuffer[::-1])
                if atom == ns.quote:
                    return True
                buffer.append(atom) 
            atombuffer = ''
        else:
            atombuffer += char
    return False
    

def print_list(buffer):
    if (type(buffer) == type([]) or  type(buffer) == type(())) and len(buffer) > 1:
        _str = '('
        for item in buffer:
            _str += ' ' + str(item)
        _str += ' )'
    else:
        _str = buffer
    print(_str)


def parse(buffer):
    if callable(buffer[0]):
        func = buffer[0]
        args = buffer[1:][::-1]
        return func(*args)
    elif isList:
        return tuple(buffer[::-1])
    else:
        return buffer

def reset():
    global stack
    global buffer
    global atombuffer
    global isString
    stack = deque()
    buffer = []
    atombuffer = ''
    isString = False


def repl():
    global buffer
    global atombuffer
    while True:
        reset()
        try: 
            command = input(">>>")
            is_quote = False
            quote = ''
            for char in reversed(command):
                if is_quote:
                    quote += char
                else:
                    is_quote = tolkenize(char)
            if is_quote:
                print(quote[::-1])
            else:
                if atombuffer:
                    buffer.append(types.cast(atombuffer[::-1]))
                print("buffer: ",buffer)
                print("buffer[0]: ",buffer[0])
                if type(buffer[0]) == type([]):
                    print("buffer[0][::-1]: ",buffer[0][::-1])
                    print_list(buffer[0][::-1])
                else:
                    print_list(buffer[0])
        except EOFError: break


def read_file(filename):
    global atombuffer
    global buffer
    with open(filename) as lisp_file:
        for line in lisp_file:
            for char in reversed(line):
                tolkenize(char)
    if atombuffer:
        buffer.append(types.cast(atombuffer[::-1]))
    print_list(buffer[0][::-1])


def main(*args, **kwargs):
    reset()
    args = [item for sublist in args for item in sublist]
    if not len(args):
        return repl()
    filename = args[0]
    return read_file(filename)


if __name__ == "__main__":
    main(sys.argv[1:])