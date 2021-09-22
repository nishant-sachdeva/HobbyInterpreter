from strings_with_arrows import string_with_arrows

# ERRORS
class Error:
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = str(self.error_name) + ":" + str(self.details)
        result += " " + str(self.pos_start.file_name) + " line : "+  str(self.pos_start.ln + 1)
        result += '\n\n' + string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'IllegalWordError', details)


class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class RTError(Error):
    def __init__(self, pos_start, pos_end, details, context):
        super().__init__(pos_start, pos_end,'Runtime Error', details)
        self.context = context
    
    def as_string(self):
        result = self.generate_trackeback()
        result += str(self.error_name) + ":" + str(self.details)
        result += '\n\n' + string_with_arrows(self.pos_start.file_text, self.pos_start, self.pos_end)
        return result

    def generate_trackeback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context

        while ctx:
            result += "File " + str(pos.file_name) + " line : "+  str(pos.ln + 1) + " in " + str(ctx.display_name) + "\n"
            pos = ctx.parent_entry_pos
            ctx = ctx.parent

        return "Traceback : Most recent last call \n" + result
