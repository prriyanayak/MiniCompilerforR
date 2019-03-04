import ply.lex as lex

reserved = {
   'while': 'WHILE',
   'for': 'FOR',
   'break': 'BREAK',
   'True': 'TRUE',
   'False' : 'FALSE',
   'in' : 'IN',
   'print' : 'PRINT'	
}

comparators = ['LESSTHAN','GREATERTHAN','EQUALS','NOTEQUALS','LESSTHANOREQUAL','GREATERTHANOREQUAL']
unary = ['DECREMENT','INCREMENT']
literals = ['[', ']', '~', '$']
assignments = ['<-','->','<<-','->>',':=', '=']
tokens = ['UNARY',
        'COMPARATORS',
        'LBRACE',
        'RBRACE',
        'AND',
        'OR',
        'ASSIGNMENTS',
        'RSQUARE',
        'LSQUARE',
        'LITERALSTRING',
        'LPAREN',
        'RPAREN',
        'NUMBER',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',
        'ID',
        'COLON'
    ] + list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS= r'\+'
t_MINUS= r'-'
t_TIMES= r'\*'
t_DIVIDE= r'/'
t_LPAREN= r'\('
t_RPAREN= r'\)'
t_LBRACE=r'\{' 
t_RBRACE=r'\}' 
t_LITERALSTRING=r'\".*\"'
t_AND=r'&&'
t_OR=r'\|\|'
t_RSQUARE=r'\]'
t_LSQUARE=r'\['
t_COLON = r':'

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    )

def t_UNARY(t):
    r'( \+\+ | -- )'
    t.type='UNARY'    #this return type should match names from tokens[] list!important
    return t

def t_ASSIGNMENTS(t):
	r'( \<\- | \-\> | = | \<\<\- | \-\>\> | \:\=)'
	t.type = 'ASSIGNMENTS'
	return t


def t_COMPARATORS(t):
    r'( < | > | >= | <= | == | != )'
    t.type = 'COMPARATORS'
    return t



def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')
    return t


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()
