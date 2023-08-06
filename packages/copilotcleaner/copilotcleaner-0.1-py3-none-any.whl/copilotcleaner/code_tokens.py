import tokenize

class CodeTokens:
    def __init__(self, file_path):
        self.__file_path = file_path
        
    def get_tokens(self):
        with open(self.__file_path, 'r') as file:
            yield tokenize.generate_tokens(file.readline)

