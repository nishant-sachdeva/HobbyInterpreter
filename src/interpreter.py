from constants import *
from errors import RTError

class RTResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self ,res):
        if res.error:
            self.error = res.error
        return res.value
    
    def success(self , value):
        self.value = value
        return self

    def failure(self , error):
        self.error = error
        return self


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()
    
    def set_pos(self, pos_start = None, pos_end = None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    
    def set_context(self, context=None):
        self.context = context
        return self

    def copy(self):
        copy = Number(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def added_to(self, other):
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None
        
    def subbed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None
    
    def multed_by(self, other):
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None
    
    def divided_by(self, other):
        if isinstance(other, Number):
            if other.value == 0:
                return None, RTError(other.pos_start, other.pos_end, 'Division by Zero', self.context)
            else:
                return Number(self.value / other.value).set_context(self.context), None

    def power_to(self,other):
        if isinstance(other,Number):
            return Number(self.value ** other.value).set_context(self.context), None

    def get_comparison_eq(self, other):
        if isinstance(other,Number):
            return Number(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_ne(self, other):
        if isinstance(other,Number):
            return Number(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_lt(self, other):
        if isinstance(other,Number):
            return Number(int(self.value < other.value)).set_context(self.context), None
    
    def get_comparison_gt(self, other):
        if isinstance(other,Number):
            return Number(int(self.value > other.value)).set_context(self.context), None
    
    def get_comparison_lte(self, other):
        if isinstance(other,Number):
            return Number(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_gte(self, other):
        if isinstance(other,Number):
            return Number(int(self.value >= other.value)).set_context(self.context), None
    
    def anded_by(self, other):
        if isinstance(other,Number):
            return Number(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other,Number):
            return Number(int(self.value or other.value)).set_context(self.context), None    

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def __str__(self):
        return str(self.value)


class Context:
    def __init__(self, display_name, parent = None, parent_entry_pos=None):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table = None



class Interpreter:
    def visit(self,node, context):
        method_name = "visit_" + str(type(node).__name__)
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception("No visit_" + str(type(node).__name__) + " method defined")
    
    def visit_NumberNode(self, node, context):
        return RTResult().success(Number(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_VarAssignNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = res.register(self.visit(node.value, context))
        if res.error:
            return res

        context.symbol_table.set(var_name, value)
        return res.success(value)

    def visit_VarAccessNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        value = context.symbol_table.get(var_name)

        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end, var_name+ " is not defined", context))

        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)

    def visit_BinOpNode(self,node, context):
        res = RTResult()

        left = res.register(self.visit(node.left_node, context))
         
        if res.error:
            return res
        
        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res
        
        if node.op_tok.type == TT_PLUS:
            result, error = left.added_to(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.subbed_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.multed_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.divided_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.power_to(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.matches(TT_KEYWORD, 'AND'):
            result, error = left.anded_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'OR'):
            result, error = left.ored_by(right)

        
        if error:
            return res.failure(error)

        return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))

        if res.error:
            return res
        
        error = None

        if node.op_tok.type == TT_MINUS:
            number,error = number.multed_by(Number(-1))

        if node.op_tok.matches(TT_KEYWORD, 'NOT'):
            number, error = number.notted()
        
        if error:
            return res.failure(error)
        
        return res.success(number.set_pos(node.pos_start, node.pos_end))

        

