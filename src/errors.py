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
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'IllegalWordError', details)

