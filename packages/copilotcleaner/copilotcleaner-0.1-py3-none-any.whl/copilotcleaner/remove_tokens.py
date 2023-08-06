from os import stat
from .code_tokens import CodeTokens

class RemoveTokens():
    @staticmethod
    def remove_copilot_comments(file_path):
        code_tokens = CodeTokens(file_path)

        final_code = ""
        previous_line = ""

        for tokens in code_tokens.get_tokens():
            for token in tokens:
                # If token's type is not 60 (comment) and line does not start with "#$" then add to final_code
                if token.type != 60 and not token.line.strip().startswith("#$"):
                    if previous_line != token.line:
                        final_code += token.line
                    previous_line = token.line

        with open(file_path, "w") as file:
            file.write(final_code)
