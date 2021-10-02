from lexer import Lexer
from parser import Parser
from interpreter import Interpreter, Context, Number
from symbols import SymbolTable


global global_symbol_table
global_symbol_table = SymbolTable()
global_symbol_table.set("null", Number(0))

#  RUN FUNCTION:
def run_command(file_name, text):

    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()


    if error:
        print("There was an error")
        return None, error

    parser_object = Parser(tokens)

    ast = parser_object.parse()

    if ast.error:
        return None, ast.error

    interpreter_object = Interpreter()
    
    context = Context('<program>')
    context.symbol_table = global_symbol_table
    
    result = interpreter_object.visit(ast.node, context)

    return result.value , result.error