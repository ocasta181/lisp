import lisp_namespace as ns

class AST():

    def __init__(self):
        self.root = ASNode(ns._return)
        self.current = self.root

    def setCurrent(self, ASNode):
        self.current = ASNode

    def __str__(self):
        def build_tree(node):
            if len(node.children):
                _tree = []
                for child in node.children:
                    _tree.append(build_tree(child))
                return {node.val: _tree}
            else:
                return node.val
        tree = build_tree(self.root)
        return str(tree)
                


class ASNode():

    def __init__(self, val, parent = None):
        self.val = val
        self.parent = parent
        self.children = []

    def addChild(self, node):
        self.children.append(node)
        node.parent = self
        return node

    def __str__(self):
        return str(self.val)