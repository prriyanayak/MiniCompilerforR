import plyLex
import sys

# if len(sys.argv) < 2:
#     print("Please Enter the name of the Source file")
#     exit(0)
data = open("ex2.r","r")

data = data.read()
tokens = plyLex.generateToken(data)

symbolTable = dict()
currentTable = symbolTable
stack = list()
stack.append(currentTable)
entry = 1

for t in tokens:
    if t.value != '{' and t.value != '}':
        if t.value not in stack[-1]:
            stack[-1][t.value] = [t.type,t.lineno]
    elif t.value == '{':
        currentTable = stack[-1]['scope'+str(entry)] = dict()   #using to the advantage of shallow copy....i.e we create a reference
        stack.append(currentTable)
        entry+=1

    elif t.value ==  '}':
        stack.pop()
        if len(stack) == 0:
            stack.append(symbolTable)

for k,v in symbolTable.items():
    print(k,"  ",v)