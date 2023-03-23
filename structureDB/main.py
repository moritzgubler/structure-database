import argparse
from ase.io import read, write
import structureDB.initialize_db
import structureDB.convexHull
import structureDB.add
import sys
import numpy as np

def main():
    
    parser = argparse.ArgumentParser(description = 
        """
        Welcome to structureDB. This program organizes structures using the ASE IO functions and organizes them.
        """ 
    )
    subparsers = parser.add_subparsers(help="Command that database will execute", dest='command', required=True)
    add_parser = subparsers.add_parser("add", help="Add a list of files to the database")
    conv_parser = subparsers.add_parser("convexHull", help = "Calculate a convex hull plot")
    init_parser = subparsers.add_parser("init", help = "Initialize a structure database in the current working derectory")
    get_parser = subparsers.add_parser("get", help="Get files from database")

    add_parser.add_argument('files', type=argparse.FileType('r'), nargs=argparse.REMAINDER)

    get_parser.add_argument( '-e', '--ediff', type=float, help="Filter by energy difference per atom", dest='ediff',
        required=False, default=np.inf)
    get_parser.add_argument('-n', '--nmax', type=int, help="Maximal elements of each stoichiometry",
        dest='nmax', default=np.inf, required=False)
    get_parser.add_argument('-o', '--outdir', type=str, help="Output directory will be cleaned up before use. Default is output/",
        dest='outdir', default='output', required=False) 
    get_parser.add_argument('-t', '--extension', type=str, default='extxyz', dest='ext', 
        required=False, choices=['ascii, extxyz', 'in'], help="File format of output files.")

    args = parser.parse_args()

    if args.command == 'init':
        structureDB.initialize_db.initialize()
    elif not structureDB.initialize_db.isInitialized():
        print("Database must be initialized first")
        sys.exit(1)

    if args.command == 'add':
        structureDB.add.add_files(args.files)
    if args.command == 'convexHull':
        print('Calculating convex hull')


