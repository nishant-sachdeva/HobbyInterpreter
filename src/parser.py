from constants import *
from errors import InvalidSyntaxError
from nodes import *

class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None
        self.advance_count = 0

    def register_advancement(self):
        self.advance_count += 1
        return

    def register(self, res):
        self.advance_count += res.advance_count
        if res.error:
            self.error = res.error
        return res.node

    def success(self, node):
        self.node = node
        return self
        
    def failure(self, error):
        if not self.error or self.advance_count == 0:
            self.error = error
        return self

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expression()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure( InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected '+', '-', '*' or '/' "))
        return res

    def atom(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_INT, TT_FLOAT):
            res.register_advancement()
            self.advance()
            return res.success(NumberNode(tok))
        
        elif tok.type == TT_IDENTIFIER:
            res.register_advancement()
            self.advance()
            return res.success(VarAccessNode(tok))

        elif tok.type == TT_LPAREN:
            res.register_advancement()
            self.advance()
            expr = res.register(self.expression())
            if res.error:
                return res
            
            if self.current_tok.type == TT_RPAREN :
                res.register_advancement()
                self.advance()
                return res.success(expr)
            else:
                return res.failure( InvalidSyntaxError(self.current_tok.pos_start , self.current_tok.pos_end, "Expected ')' "))

        elif tok.matches(TT_KEYWORD, 'IF'):
            if_expr = res.register(self.if_expr())
            if res.error:
                return res
            return res.success(if_expr)

        elif tok.matches(TT_KEYWORD, 'FOR'):
            for_expr = res.register(self.for_expr())
            if res.error:
                return res
            return res.success(for_expr)

        elif tok.matches(TT_KEYWORD, 'WHILE'):
            while_expr = res.register(self.while_expr())
            if res.error: return res

            return res.success(while_expr)

        return res.failure(InvalidSyntaxError(tok.pos_start , tok.pos_end, "Expected int , float, identifier +, - or ("))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'FOR'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start , self.current_tok.pos_end, "Expected FOR"))

        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start , self.current_tok.pos_end, "Expected Identifier"))

        var_name = self.current_tok
        res.register_advancement()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected = "))

        res.register_advancement()
        self.advance()

        start_value = res.register(self.expression())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'TO'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected TO"))

        res.register_advancement()
        self.advance()

        end_value = res.register(self.expression())

        step_value = None
        if self.current_tok.matches(TT_KEYWORD, 'STEP'):
            res.register_advancement()
            self.advance()

            step_value = res.register(self.expression())

            if res.error:
                return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected THEN"))

        res.register_advancement()
        self.advance()
        
        body_value = res.register(self.expression())
        if res.error:
            return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body_value))


    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'WHILE'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected WHILE"))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected THEN"))

        res.register_advancement()
        self.advance()

        body = res.register(self.expression())
        if res.error: return res

        return res.success(WhileNode(condition, body))    


    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, 'IF'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected IF"))

        res.register_advancement()
        self.advance()

        condition = res.register(self.expression())
        if res.error:
            return res
        
        if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start,self.current_tok.pos_end, "Expected THEN"))

        res.register_advancement()
        self.advance()

        expr = res.register(self.expression())
        if res.error:
            return res
        cases.append((condition, expr))

        while self.current_tok.matches(TT_KEYWORD, 'ELIF'):
            res.register_advancement()
            self.advance()

            condition = res.register(self.expression())
            if res.error:
                return res

            if not self.current_tok.matches(TT_KEYWORD, 'THEN'):
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected THEN"))

            res.register_advancement()
            self.advance()

            expr = res.register(self.expression())
            if res.error:
                return res
            cases.append((condition, expr))

        if self.current_tok.matches(TT_KEYWORD, 'ELSE'):
            res.register_advancement()
            self.advance()

            else_case = res.register(self.expression())
            if res.error:
                return res

        return res.success(IfNode(cases, else_case))

    def power(self):
        return self.binary_op(self.atom, (TT_POW, ) , self.factor)

    def factor(self):
        res = ParseResult()
        tok = self.current_tok
        if tok.type in (TT_PLUS, TT_MINUS):
            res.register_advancement()
            self.advance()
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power() 

    def term(self):
        return self.binary_op(self.factor, (TT_MUL, TT_DIV))


    def expression(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'VAR'):
            res.register_advancement()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start , self.current_tok.pos_end, "Expected identifier"))

            var_name = self.current_tok
            res.register_advancement()
            self.advance()
            
            if self.current_tok.type != TT_EQ:
                return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected = "))
            
            res.register_advancement()
            self.advance()
            
            expr = res.register(self.expression())
            if res.error :
                return res
            return res.success(VarAssignNode(var_name, expr))

        node = res.register(self.binary_op(self.comp_expr , ((TT_KEYWORD, "AND"), (TT_KEYWORD, "OR"))))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected VAR, int, float, identifier, +, -, or ( " ))

        return res.success(node)

    def binary_op(self, func_a, ops, func_b=None):
        if func_b == None:
            func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        
        if res.error:
            return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()
            right = res.register(func_b())

            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

    
    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'NOT'):
            op_tok = self.current_tok
            res.register_advancement()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error:
                return res

            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.binary_op(self.arith_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_tok.pos_start, self.current_tok.pos_end, "Expected int, float, identifier,+, -, (, NOT "))


        return res.success(node)

    def arith_expr(self):
        return self.binary_op(self.term, (TT_PLUS, TT_MINUS))