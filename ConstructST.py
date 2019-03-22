import plyLex
import sys
# import math

# if len(sys.argv) < 2:
#     print("Please Enter the name of the Source file")
#     exit(0)


f = open(sys.argv[1])
data = f.read()
tokens = plyLex.generateToken(data)

symbolTable = dict()
currentTable = symbolTable
stack = list()
stack.append(currentTable)
entry = 1

for t in tokens:
    # print(t)
    # print(type(t.value))
    # print(symbolTable)
    # print(currentTable)
    # print(t.value)
    if (t.type != "ID"):
        continue
    else:
    	if t.value != '{' and t.value != '}':
        	if t.value not in stack[-1]:
        		stack[-1][t.value] = [t.type, t.lineno, -1, -1]
    	elif t.value == '{':
    	    currentTable = stack[-1]['scope'+str(entry)] = dict()   #using to the advantage of shallow copy....i.e we create a reference
    	    stack.append(currentTable)
    	    entry+=1

    	elif t.value ==  '}':
        	stack.pop()
        	if len(stack) == 0:
        		stack.append(symbolTable)

print("NAME TOKEN LINE NO. INITIAL VALUE TYPE OF ATTRIBUTE")
for k,v in symbolTable.items():
    print(k,"  ",v)