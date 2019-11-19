#!/usr/bin/env python3

# Postfix Lisp

import sys, re
import lisp_namespace as ns
import lisp_types as types
import lisp_ast as ast

def tolkenize(file):
    tolken = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    return [t for t in re.findall(tolken, file) if t[0] != ';']
    

def graph(tolkens):
    AST = ast.AST()
    depth = 0
    tree_buffer = [[]]
    depth_start = [0]
    for idx,tolken in enumerate(tolkens):
        print('tree_buffer: ',tree_buffer)
        print('depth: ',depth)
        # print('tree_buffer['+str(depth)+']: ',tree_buffer[depth])  
        if tolken == '(':
            print('depth++')
            depth += 1
            tree_buffer.append([])
            depth_start.append(idx)
        elif tolken == ')':
            print('depth--')
            depth -= 1
            depth_start.pop()
            tree_buffer[depth].extend(tree_buffer[depth+1])
            print('pre pop tree_buffer: ',tree_buffer)
            tree_buffer.pop()
            print('popped tree_buffer: ',tree_buffer)
            if depth == 0:
                for node in tree_buffer[0]:
                    AST.root.addChild(node)
        else:
            tolken = types.cast(tolken) 
            node = ast.ASNode(tolken)

            if callable(tolken):
                print('handle function')
                if tolken == ns.functions['quote']:
                    print('handle quote')
                    tree_buffer[depth] = [node]
                    node.children = [ast.ASNode(tolken) for tolken in tolkens[depth_start[depth]+1: idx]]
                    print('tolkens to quote: ',tolkens[depth_start[depth]: idx])
                else:
                    node.children = tree_buffer.pop()
                    tree_buffer.append([node])
                    
            else:
                print('handle atom')
                tree_buffer[depth].append(node)
    return AST


def Eval(node):
    resolved_children = []
    if node.val == ns.functions['cond']:
        handle_cond(node, resolved_children)
    elif node.val == ns.functions['lambda']:
        handle_lambda(node, resolved_children)
    else:
        while node.children:
            child = node.children.pop(0)
            resolved_children.append(Eval(child))

    if callable(node.val):
        return node.val(*resolved_children)
    else:
        node.children = []
        return node.val
    


def handle_lambda(node, resolved_children):
    if len(node.children) != 2:
        raise ValueError
    # else:
    #     params = node.children[0]
    #     body = node.children[1]
    #     lambda 
    #     node.val
    #     print("params: ",params)
    #     print("body: ",body)


def handle_cond(node, resolved_children):
    last = False
    for idx,child in enumerate(node.children):
        if idx % 2 != 0:
            continue
        elif last == False and child == ns.symbols['else']:
            resolved_children.append(Eval(children[idx+1]))
        else:
            res = Eval(child)
            if res:
                last = True
                resolved_children.append(Eval(node.children[idx+1]))
            else:
                last = False
    

def repl():
    while True:
        try: 
            command = input(">>>")
            Eval(read(command).root)
        except EOFError: break


def read_file(filename):
    with open(filename) as lisp_file:
        read(lisp_file.read())


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