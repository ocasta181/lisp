#!/usr/bin/env python3

# Postfix Lisp

import sys, re
from collections import deque
import lisp_namespace as ns
import lisp_types as types
import lisp_ast as ast

def tolkenize(file):
    tolken = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    return [t for t in re.findall(tolken, file) if t[0] != ';']
    

def graph(tolkens, AST):
    depth = 0
    for idx,tolken in reversed(list(enumerate(tolkens))):
        if tolken == '(':
            if depth > 0:
                AST.setCurrent(AST.current.parent)
            depth -= 1
        elif tolken != ')':
            tolken = types.cast(tolken)
            if callable(tolken):
                AST.setCurrent(AST.current.addChild(ast.ASNode(tolken)))
                depth += 1
            else:
                AST.current.addChild(ast.ASNode(tolken))

def execute(node):
    resolved_children = []
    while node.children:
        child = node.children.pop(0)
        resolved_children.append(execute(child))
    if callable(node.val):
        return node.val(*resolved_children[::-1])
    else:
        node.children = []
        return node.val
    

def repl():
    while True:
        try: 
            command = input(">>>")
            read(command)
        except EOFError: break


def read_file(filename):
    with open(filename) as lisp_file:
        read(lisp_file.read())


def read(data):
    AST = ast.AST()
    tolkens = tolkenize(data)
    graph(tolkens, AST)
    execute(AST.root)


def main(*args, **kwargs):
    args = [item for sublist in args for item in sublist]
    if not len(args):
        return repl()
    filename = args[0]

    return read_file(filename)


if __name__ == "__main__":
    main(sys.argv[1:])