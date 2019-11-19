#!/usr/bin/env python3

# Postfix Lisp

import sys, re
import lisp_namespace as ns
import lisp_types as types

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
            if callable(types.cast(tolken)):
                if tolken == 'quote':
                    tree_buffer[depth] = {tolken: [tolken for tolken in tolkens[depth_start[depth]+1: idx]]}
                else:
                    children = tree_buffer.pop()
                    tree_buffer.append({tolken: children})
                    
            else:
                tree_buffer[depth].append(tolken)
    return tree_buffer[0]


def eval_ast(ast):
    resolved_children = []
    if isinstance(ast, list):
        ns._return(*ast)
    elif isinstance(ast, dict):
        for parent, children in ast.items():
            parent = types.cast(parent)
            if parent == ns.functions['cond']:
                handle_cond(children, resolved_children)
            elif parent == ns.functions['lambda']:
                handle_lambda(children, resolved_children)
            elif parent == ns.functions['quote']:
                return parent(*children)
            else:
                while children:
                    child = children.pop(0)
                    resolved_children.append(eval_ast(child))

            if callable(parent):
                return parent(*resolved_children)
            else:
                children = []
                return parent
    else:
        return types.cast(ast)


def Eval(AST):
    last = 0
    for item in AST:
        if isinstance(item, (list,dict)):
            last = eval_ast(item)
        else:
            last = types.cast(item)
    return last
   

def handle_lambda(children, resolved_children):
    if len(children) != 2:
        raise Exception('lambdas require two parameters, first: a parameter list, second: a function body')
    # else:
    #     params = node.children[0]
    #     body = node.children[1]
    #     lambda 
    #     node.val
    #     print("params: ",params)
    #     print("body: ",body)


def handle_cond(children, resolved_children):
    last = False
    for idx,child in enumerate(children):
        if idx % 2 != 0:
            continue
        elif last == False and child == ns.symbols['else']:
            resolved_children.append(Eval(children[idx+1]))
        else:
            res = Eval(child)
            if res:
                last = True
                resolved_children.append(Eval(children[idx+1]))
            else:
                last = False
    

def repl():
    while True:
        try: 
            command = input(">>>")
            print(Eval(read(command)))
        except EOFError: break


def read_file(filename):
    with open(filename) as lisp_file:
        print(Eval(read(lisp_file.read())))


def read(data):
    tolkens = tolkenize(data)
    return graph(tolkens)


def main(*args, **kwargs):
    args = [item for sublist in args for item in sublist]
    if not len(args):
        return repl()
    filename = args[0]

    return read_file(filename)


if __name__ == "__main__":
    main(sys.argv[1:])