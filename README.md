# MiniCompilerforR

### File Descriptions - 
- ex.r - contains the original code.
- ex1.r - code without comments or newlines
- removeComments.py - removes comments and newlines
- plyLex.py - Lex code to generate Tokens
- YaccOnly.py - Yacc code that generates parseTree + intermediate Code

### To run - 
1. python3 removeComments.py
2. python3 -W ignore YaccOnly.py ex1.r

