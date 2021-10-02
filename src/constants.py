# TOKENS
TT_INT    = 'TT_INT'
TT_FLOAT  = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD = 'KEYWORD'
TT_PLUS   = 'PLUS'
TT_MINUS  = 'MINUS'
TT_MUL    = 'MUL'
TT_DIV    = 'DIV'
TT_POW    = 'POW'
TT_EQ     = 'EQ'
TT_LPAREN = 'LPAREN'
TT_RPAREN = 'RPAREN'
TT_EOF    = 'EOF'

import string
LETTERS = string.ascii_letters

# CONSTANTS
DIGITS = '0123456789'

LETTERS_DIGITS = DIGITS + LETTERS + '_'

KEYWORDS = ['FOR', 'IF', 'ELSE', 'VAR']