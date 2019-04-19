import ply.yacc as yacc
from plyLex import tokens
from plyLex import main_table
import sys


class bcolors:
	GREEN = '\033[92m'
	RED = '\033[91m'
	WHITE = '\033[0m'
	PURPLE = '\033[35m'

tokens = tokens
parseTree = ()
icg = []
tempCount = 1
currTemp = ""
labelCount = 1
labels = []
expr_val = []


def innerMost(x):
	f = 1
	while (f == 1):
		if type(x) == tuple:
			x = x[-1]
		else: 
			f = 0
	return x

def p_error(p):
	print (bcolors.RED+"Something went wrong"+bcolors.WHITE)
	print (bcolors.RED+"Error at "+str(p.lineno)+bcolors.WHITE)
	exit()

def p_start(p):
    '''start : assign
      | statement
      | assign start
      | statement start
      | forLoop start
      | forLoop if
      | if forLoop
      | if
      | if start'''
    if len(p)==2:
        p[0]=('START',p[1])
    elif len(p)==3:
        p[0]=('START',p[1],p[2])
    else:
        p[0]=('START',p[1],p[2],p[3])      
    global parseTree
    parseTree = p[0]

def p_assign(p):
    '''assign : factor ASSIGNMENTS expr '''
    p[0]=('ASSIGN',p[1],"ASSIGNED TO",p[3])
    global currTemp
    global icg
    global tempCount
    if not currTemp:
        icg.append(innerMost(p[1])+" = "+str(innerMost(p[3])))
    else:
        icg.append(str(innerMost(p[1]))+" = "+str(currTemp))
    currTemp="t"+str(tempCount)
    tempCount = tempCount +1 

def p_factor(p):
    '''factor : ID
              | NUMBER '''
    
    if type(p[1])==int:
        p[0]=("FACTOR","NUM",p[1])
        # print("Type:", p[1])
    else:
        p[0]=("FACTOR","ID",p[1])
        symbol_table = main_table.get_table(main_table.inScope-1)

def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | term '''
    global currTemp
    global icg
    global tempCount
    global expr_val

    if len(p)>2 and p[2]=="+":
        if not currTemp:
            icg.append("t"+str(tempCount)+" = "+str(innerMost(p[1]))+"+"+str(innerMost(p[3])))
        else:
            if(type(innerMost(p[1]))==int):
                icg.append("t"+str(tempCount)+" = "+str(innerMost(p[1]))+" + "+str(currTemp))
            else:
                icg.append("t"+str(tempCount)+" = "+str(currTemp)+" + "+str(innerMost(p[3])))
        
        currTemp="t"+str(tempCount)
        tempCount = tempCount +1
        p[0]=('ADD',p[1],p[3])
    elif len(p)>2 and p[2]=="-":
        if not currTemp:
            icg.append("t"+str(tempCount)+"="+str(innerMost(p[1]))+" - "+str(innerMost(p[3])))
        else:
            if(type(innerMost(p[1]))==int):
                icg.append("t"+str(tempCount)+" = "+str(innerMost(p[1]))+" - "+str(currTemp))    
            else:
                icg.append("t"+str(tempCount)+" = "+str(currTemp)+" - "+str(innerMost(p[3])))
        
        currTemp="t"+str(tempCount)
        tempCount = tempCount +1
        p[0]=('SUB',p[1],p[3])
    else:
        p[0]=("EXPR",p[1])
    
def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor '''
    global currTemp
    global icg
    global tempCount
    if len(p)>2 and p[2]=="*":
        
        if not currTemp:
            icg.append("t"+str(tempCount)+"="+str(innerMost(p[1]))+"*"+str(innerMost(p[3])))
        else:
            if(type(innerMost(p[1]))==int):
                icg.append("t"+str(tempCount)+"="+str(innerMost(p[1]))+"*"+str(currTemp))    
            else:
                icg.append("t"+str(tempCount)+"="+str(currTemp)+"*"+str(innerMost(p[3])))
        
        currTemp="t"+str(tempCount)
        tempCount = tempCount +1
        p[0]=('MUL',p[1],p[3])
    elif len(p)>2 and p[2]=="/":
        
        if not currTemp:
            icg.append("t"+str(tempCount)+"="+str(innerMost(p[1]))+"/"+str(innerMost(p[3])))
        else:
            if(type(innerMost(p[1]))==int):
                icg.append("t"+str(tempCount)+"="+str(innerMost(p[1]))+"/"+str(currTemp))    
            else:
                icg.append("t"+str(tempCount)+"="+str(currTemp)+"/"+str(innerMost(p[3])))
        currTemp="t"+str(tempCount)
        tempCount = tempCount +1
        p[0]=('DIVIDE',p[1],p[3])
    else:
        p[0]=("TERM",p[1])

def p_statement(p): 
	'''statement : PRINT LPAREN factor RPAREN'''
	p[0]="STATEMENT"
	global icg
	global labels
	if len(labels)>1:
		icg.append("goto "+labels[-1])
		labels=labels[0:-1]
		icg.append(labels[-1]+":")
		labels=labels[0:-1]
	icg.append(" STMT ")

def p_statementnew(p):
	'''statementnew : LBRACE PRINT LPAREN factor RPAREN RBRACE'''
	p[0] = ("PRINT", p[4])
	global icg
	global labels
	if len(labels)>1:
		icg.append("goto "+labels[-1])
		labels=labels[0:-1]
		icg.append(labels[-1]+":")
		labels=labels[0:-1]
	icg.append(" PRINT ")

def p_if(p):
    '''if : IF LPAREN expr COMPARATORS expr RPAREN statementnew else'''
    p[0] = ('IF', p[2], p[3], p[4], p[5], p[6], p[7], p[8])

def p_else(p):
    '''else : ELSE statementnew'''
    p[0] = ('ELSE', p[2])


def p_forLoop(p):
	'''forLoop : FOR inner'''
	p[0] = ('FOR', p[2])

def p_inner(p):
	'''inner : LPAREN ID IN range RPAREN statementnew'''
	p[0] = ('INSIDE FOR', p[1], p[2], p[3], p[4], p[5], p[6])

def p_range(p):
	'''range : LPAREN factor COLON factor RPAREN 
			 | factor COLON factor
	'''
	global icg
	global labels
	global labelCount
	if (len(p) == 6):
		p[0] = ('RANGE', p[1], p[2], p[3], p[4], p[5])
		icg.append(str(innerMost(p[-2]))+"="+str(innerMost(p[2])))
		icg.append("L"+str(labelCount)+":")
		labelCount = labelCount + 1

		icg.append("ifFalse "+str(innerMost(p[-2]))+"<"+str(innerMost(p[4]))+" goto L"+str(labelCount))
		labels.append("L"+str(labelCount))
		labels.append("L"+str(labelCount-1))
		labelCount = labelCount + 1
	elif (len(p) == 4):
		p[0] = ('RANGE', p[1], p[2], p[3])
		icg.append(str(innerMost(p[-2]))+"="+str(innerMost(p[1])))
		icg.append("L"+str(labelCount)+":")
		labelCount = labelCount + 1

		icg.append("ifFalse "+str(innerMost(p[-2]))+"<"+str(innerMost(p[3]))+" goto L"+str(labelCount))
		labels.append("L"+str(labelCount))
		labels.append("L"+str(labelCount-1))
		labelCount = labelCount + 1



def printParseTree(s):
	tabs=-1
	finalStr=""
	toBeIgnore=[',','\'']
	symbols=['=','+','-','*','/',':', '<']
	
	# print(s)
	for i in range(0,len(s)):
		if s[i]=="(":
			finalStr = finalStr+"\n"
			tabs = tabs+1
			for j in range(0, tabs):
				finalStr = finalStr + bcolors.WHITE+"---"
		elif s[i]==")":
			tabs = tabs-1
			finalStr=finalStr+"\n"
		else:
			if s[i] not in toBeIgnore:
				if s[i] in symbols:
					for j in range(0, tabs):
						finalStr=finalStr+bcolors.WHITE+"---"
					finalStr=finalStr+"  "+bcolors.PURPLE+s[i]+bcolors.WHITE
				else:
					finalStr=finalStr+bcolors.PURPLE+s[i]+bcolors.WHITE
				if s[i]=="T" and s[i-1]=="N":
					finalStr=finalStr+"\n"
	return finalStr


parser = yacc.yacc()

f = open(sys.argv[1])
data = f.read()

res = yacc.parse(data)
main_table.print_table()
# print(expr_val)
# print (bcolors.GREEN+"PARSE TREE"+bcolors.WHITE)
# print("\n\n\n")c
# print (parseTree)
# print ("\n")
print (printParseTree(str(parseTree)))


# print ("\n\n")
print (bcolors.GREEN+"ICG "+bcolors.WHITE)
for i in icg:
    print(i)

# print ("\n")