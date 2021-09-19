from lexer import Lexer
from parser import Parser

#  RUN FUNCTION:

def run_command(file_name, text):

    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    if error:
        print("There was an error")
        return None, error

    parser_object = Parser(tokens)
    ast = parser_object.parse()

    return ast.node, ast.error