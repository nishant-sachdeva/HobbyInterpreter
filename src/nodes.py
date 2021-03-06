class NumberNode:
    def __init__(self, token):
        self.tok = token
        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end

    def __repr__(self):
        return str(self.tok)


class BinOpNode:
    def __init__(self,left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return "(" + str(self.left_node) + " "  + str(self.op_tok) + " " + str(self.right_node) + ")"


class UnaryOpNode:
    def __init__(self,op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return "(" + str(self.op_tok) + " , " + str(self.node) + ")"


class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

class ForNode:
    def __init__(self,var_name_tok, start_value_node, end_value_node, step_value_node, body_node):
        self.var_name_tok = var_name_tok
        self.start_value = start_value_node
        self.end_value = end_value_node
        self.step_value = step_value_node
        self.body = body_node

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body.pos_end


class WhileNode:
    def __init__(self, condition_node, body_node):
        self.condition = condition_node
        self.body = body_node

        self.pos_start = self.condition.pos_start
        self.pos_end = self.body.pos_end


class VarAccessNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


class VarAssignNode:
    def __init__(self, var_name_tok,value):
        self.var_name_tok = var_name_tok
        self.value = value
        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end


