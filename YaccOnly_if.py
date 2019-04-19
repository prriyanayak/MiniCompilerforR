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
	  | if
	  '''
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

def p_factor(p):
	'''factor : ID
			  | NUMBER '''
	
	if type(p[1])==int:
		p[0]=("FACTOR","NUM",p[1])
	else:
		p[0]=("FACTOR","ID",p[1])
		symbol_table = main_table.get_table(main_table.inScope-1)

def p_expr(p):
	'''expr : expr PLUS term
			| expr MINUS term
			| term '''
	if len(p)>2 and p[2]=="+":
		p[0]=('ADD',p[1],p[3])
	elif len(p)>2 and p[2]=="-":
		p[0]=('SUB',p[1],p[3])
	else:
		p[0]=("EXPR",p[1])
	
def p_term(p):
	'''term : term TIMES factor
			| term DIVIDE factor
			| factor '''
	if len(p)>2 and p[2]=="*":
		p[0]=('MUL',p[1],p[3])
	elif len(p)>2 and p[2]=="/":
		p[0]=('DIVIDE',p[1],p[3])
	else:
		p[0]=("TERM",p[1])

def p_statement(p): 
	'''statement : PRINT LPAREN factor RPAREN'''
	p[0]="STATEMENT"

def p_statementnew(p):
	'''statementnew : LBRACE PRINT LPAREN factor RPAREN RBRACE'''
	p[0] = ("PRINT", p[4])


def p_if(p):
	'''if : IF LPAREN expr COMPARATORS expr RPAREN statementnew else'''
	p[0] = ('IF', p[2], p[3], p[4], p[5], p[6], p[7], p[8])

def p_else(p):
	'''else : ELSE statementnew'''
	p[0] = ('ELSE', p[2])



def printParseTree(s):
	tabs=-1
	finalStr=""
	toBeIgnore=[',','\'']
	symbols=['=','+','-','*','/',':', '<', '>']
	

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

print(printParseTree(str(parseTree)))

# for i in parseTree:
# 	if i == "START":
# 		print(i, "\n\n")
# 	else:
# 		for j in i:
# 			print(j, "\n\n")