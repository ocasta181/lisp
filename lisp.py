#!/usr/bin/env python3

# Postfix Lisp

import sys, re
import lisp_environment as env
import lisp_builtins as _global
import lisp_types as types


_globals = { 
    '+': _global.add,
    '-': _global.sub,
    '*': _global.mult,
    '/': _global.div,
    'eq?': _global.eq,
    'quote': _global.quote,
    'cons': _global.cons,
    'car': _global.car,
    'cdr': _global.cdr,
    'atom?': _global.atom,
    'def': _global.define,
    'lambda': _global.lambdef,
    'cond': _global.cond,
    '_return': _global._return,
    'else': 'else'
}

def tolkenize(file):
    tolken = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    return [t for t in re.findall(tolken, file) if t[0] != ';']
    

def graph(tolkens):
    depth = 0
    tree_buffer = [[]]
    depth_start = [0]
    for idx,tolken in enumerate(tolkens):
        if tolken == '(':
            depth += 1
            tree_buffer.append([])
            depth_start.append(idx)
        elif tolken == ')':
            depth -= 1
            depth_start.pop()
            tree_buffer[depth].append(tree_buffer[depth+1])
            tree_buffer.pop()
        else:
            if tolken in _globals and callable(_globals[tolken]):
                if tolken == 'quote':
                    tree_buffer[depth] = {tolken: [tolken for tolken in tolkens[depth_start[depth]+1: idx]]}
                else:
                    children = tree_buffer.pop()
                    tree_buffer.append({tolken: children})
                    
            else:
                tree_buffer[depth].append(tolken)
    return tree_buffer[0]


def eval_ast(ast, ENV):
    resolved_children = []
    if isinstance(ast, list):
        _globals['_return'](*ast)
    elif isinstance(ast, dict):
        for parent, children in ast.items():
            parent = types.cast(parent, ENV)
            if parent == _globals['cond']:
                handle_cond(children, resolved_children, ENV)
            elif parent == _globals['lambda']:
                handle_lambda(children, resolved_children, ENV)
            elif parent == _globals['quote']:
                return parent(*children)
            else:
                while children:
                    child = children.pop(0)
                    resolved_children.append(eval_ast(child, env.environment(ENV)))

            if callable(parent):
                return parent(*resolved_children, ENV=ENV)
            else:
                children = []
                return parent
    else:
        return types.cast(ast, ENV)


def Eval(AST, ENV):
    last = 0
    for item in AST:
        last = eval_ast(item, ENV)
    return last
   

def handle_lambda(children, resolved_children, ENV):
    if len(children) != 2:
        raise Exception('lambdas require two parameters, first: a parameter list, second: a function body')


def handle_cond(children, resolved_children, ENV):
    last = False
    for idx,child in enumerate(children):
        if idx % 2 != 0:
            continue
        elif last == False and child == _globals['else']:
            resolved_children.append(Eval(children[idx+1], env.environment(ENV)))
        else:
            res = Eval(child, env.environment(ENV))
            if res:
                last = True
                resolved_children.append(Eval(children[idx+1], env.environment(ENV)))
            else:
                last = False
    

def repl():
    ENV = set_env()
    while True:
        try: 
            command = input(">>>")
            print(Eval(read(command), ENV))
        except EOFError: break


def read_file(filename):
    ENV = set_env()
    with open(filename) as lisp_file:
        print(Eval(read(lisp_file.read()),ENV))


def read(data):
    tolkens = tolkenize(data)
    return graph(tolkens)


def set_env():
    ENV = env.environment()
    for key, value in _globals.items():
        ENV.insert(key, value)

    return ENV

def main(*args, **kwargs):
    args = [item for sublist in args for item in sublist]
    if not len(args):
        return repl()
    filename = args[0]

    return read_file(filename)


if __name__ == "__main__":
    main(sys.argv[1:])