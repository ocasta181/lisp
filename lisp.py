#!/usr/bin/env python3

# Postfix Lisp

import sys, re
import lisp_namespace as ns
import lisp_types as types
import lisp_ast as ast

def tolkenize(file):
    tolken = """[\s,]*(~@|[\[\]{}()'`~^@]|"(?:[\\].|[^\\"])*"?|;.*|[^\s\[\]{}()'"`@,;]+)"""
    return [t for t in re.findall(tolken, file) if t[0] != ';']
    

def graph(tolkens, AST):
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


def execute(node):
    resolved_children = []
    if node.val == ns.functions['cond']:
            last = False
            for idx,child in enumerate(node.children):
                print('handle child:',child)
                print('idx: ',idx)
                if idx % 2 != 0:
                    print('continue')
                    continue
                elif last == False and child == ns.symbols['else']:
                    resolved_children.append(execute(children[idx+1]))
                else:
                    res = execute(child)
                    if res:
                        last = True
                        resolved_children.append(execute(node.children[idx+1]))
                    else:
                        last = False
                
            print("hit conditional")
            print("children: ",node.children)
            print('resolved_children: ',resolved_children)
    else:
        while node.children:
            child = node.children.pop(0)
            resolved_children.append(execute(child))
    if callable(node.val):
        return node.val(*resolved_children)
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
    print('tolkens: ',tolkens)
    graph(tolkens, AST)
    print('graph: ',AST)
    execute(AST.root)


def main(*args, **kwargs):
    args = [item for sublist in args for item in sublist]
    if not len(args):
        return repl()
    filename = args[0]

    return read_file(filename)


if __name__ == "__main__":
    main(sys.argv[1:])