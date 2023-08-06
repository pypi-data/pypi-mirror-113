import os
from tqdm import tqdm

from .remove_tokens import RemoveTokens

class DirWalker:
    def __init__(self, dir_path):
        self.__dir_path = dir_path

    def cleanup(self):
        py_files = []
        for root, dirs, files in os.walk(self.__dir_path):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        for file_path in tqdm(py_files, desc="Removing copilot comments"):
            RemoveTokens().remove_copilot_comments(file_path=file_path)