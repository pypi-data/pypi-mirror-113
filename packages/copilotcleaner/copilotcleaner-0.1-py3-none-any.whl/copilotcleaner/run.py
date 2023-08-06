import argparse

from .dir_walker import DirWalker

def run():
    parser = argparse.ArgumentParser(description='Copilot Comments Cleaner')
    parser.add_argument("--dir", type=str, help="Directory to project created with copilot")
    args = parser.parse_args()

    dir_walker_obj = DirWalker(args.dir)
    dir_walker_obj.cleanup()