class Token:
    def __init__(self, type_, value=None):

        self.type = type_
        self.value = value

    
    def __repr__(self):
        if self.value:
            return str(self.type) +  ":" + str(self.value)
        
        return str(self.type)

    
