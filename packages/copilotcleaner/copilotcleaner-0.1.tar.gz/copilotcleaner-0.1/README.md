# Copilot Cleaner

A simple command line tool to clean all the comments from Python project that are used by GitHub's copilot to generate code. These comments are not useful mostly and manual cleaning of these comments from large codebases is not an easy task, hence this tool.

This works only with <strong>Python</strong> projects as of now. Support for other languages will be added soon.

# Usage

```bash
user@programmer~:$ ccc -dir <path-to-project>
```

This cleans all comments that start with "#\$", so instead of just # you have to start copilot comments with "#\$".