import argparse
from ase.io import read, write

def main():
    
    parser = argparse.ArgumentParser(description = 
        """
        Welcome to structureDB. This program organizes structures using the ASE IO functions and organizes them.
        """ 
    )
    subparsers = parser.add_subparsers(help="Command that database will execute")
    add_parser = subparsers.add_parser("add", help="Add a list of files to the database")
    conv_parser = subparsers.add_parser("convexHull", help = "Calculate a convex hull plot")
    init_parser = subparsers.add_parser("init", help = "Initialize a structure database in the current working derectory")
    # get_parser = subparsers.add_parser("get", help="Deprecated")

    add_parser.add_argument('files', type=argparse.FileType('r'), nargs=argparse.REMAINDER)


    # add_args = add_parser.parse_args()
    args = parser.parse_args()

    print(args.files)