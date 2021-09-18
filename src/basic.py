from lexer import Lexer

#  RUN FUNCTION:

def run_command(file_name, text):

    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()

    return tokens, error