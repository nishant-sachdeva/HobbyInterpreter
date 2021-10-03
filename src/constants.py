# TOKENS
TT_INT        = 'TT_INT'
TT_FLOAT      = 'FLOAT'
TT_IDENTIFIER = 'IDENTIFIER'
TT_KEYWORD    = 'KEYWORD'
TT_PLUS       = 'PLUS'
TT_MINUS      = 'MINUS'
TT_MUL        = 'MUL'
TT_DIV        = 'DIV'
TT_POW        = 'POW'
TT_EQ         = 'EQ'

TT_EE         = 'EE'
TT_NE         = 'NE'
TT_LT         = 'LT'
TT_GT         = 'GT'
TT_LTE        = 'LTE'
TT_GTE        = 'GTE'

TT_LPAREN     = 'LPAREN'
TT_RPAREN     = 'RPAREN'
TT_EOF        = 'EOF'

# CONSTANTS
import string
LETTERS = string.ascii_letters
DIGITS = '0123456789'
LETTERS_DIGITS = DIGITS + LETTERS + '_'

#KEYWORDS
KEYWORDS = [
    'FOR', 
    'IF',
    'THEN',
    'ELIF',
    'ELSE', 
    'VAR',
    'AND',
    'OR',
    'NOT'
]