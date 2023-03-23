import argparse
from ase.io import read, write

def main():
    
    parser = argparse.ArgumentParser(description = 
        """
        Welcome to structureDB. This program organizes structures using the ASE IO functions and organizes them.
        """ 
    )
    subparsers = parser.add_subparsers(help="Command that database will execute")
    add_parser = subparsers.add_parser("add")
    conv_parser = subparsers.add_parser("convexHull")
    get_parser = subparsers.add_parser("get")
    args = parser.parse_args()

    print(args.command)