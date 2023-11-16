import ast
import sys

tree = ast.parse(code)

# put your code here
#with open(sys.argv[0]) as f:
#    tree = ast.parse(f.read())

nodes = ast.walk(tree)
for node in nodes:
    if type(node) is ast.Import:
        for n in node.names:
            print(n.name)