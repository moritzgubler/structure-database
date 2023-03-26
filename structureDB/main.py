import argparse
import structureDB.initialize_db
import structureDB.convexHull
import structureDB.add
import structureDB.get
import structureDB.parameters
import structureDB.convexHull
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

    conv_parser.add_argument("-p", "--onlypositions", action='store_true',
                             help="Plot positions without formation enthalpies", required=False)
    conv_parser.add_argument("-o", '--outfile', dest='outfilename', action='store', type=str,
        help='Name of the Convex hull plot file', default="enthalpies.plt", required= False)
    conv_parser.add_argument('-e1', dest='e1', action='store', type=str,
        help='Chemical symbol of first element', required= True)
    conv_parser.add_argument('-e2', dest='e2', action='store', type=str,
        help='Chemical symbol of 2nd element', required= True)
    conv_parser.add_argument('-e3', dest='e3', action='store', type=str,
        help='Chemical symbol of 3rd element', required= True)

    init_parser.add_argument('--name', dest='name', action='store', type=str,
        help='Name of the structure database directory', default="structureDB", required= False)
    init_parser.add_argument('-ns', '--n_S_orbitals', dest='ns', action='store', type=int,
        help='number of s orbitals for constructing the OMFP', default=1, required= False)
    init_parser.add_argument('-np', '--n_P_orbitals', dest='np', action='store', type=int,
        help='number of p orbitals for constructing the OMFP', default=0, required= False)
    init_parser.add_argument('-w', '--width_cutoff', dest='width_cutoff', action='store', type=float,
        help='cutoff for the OMFP', default=4.0, required= False)
    init_parser.add_argument('--maxnatsphere', dest='maxnatsphere', action='store', type=int,
        help='Truncation lentgh of the OMFP length', default=50, required= False)
    init_parser.add_argument('--fpd', dest='fpd_max', action='store', type=float,
        help='Maximal fingerprint distance between two structures that will be considered equal.', default=1e-3, required= False)
    init_parser.add_argument('--e_thresh', dest='e_thresh', action='store', type=float,
        help='Maximal energy difference per atom between two structures that will be considered equal.', default=1e-2, required= False)
    init_parser.add_argument(
        "--exclude",
        dest='exclude',
        action='store', 
        nargs="*",
        type=str,
        default=[],
        help='List of elements to exclude in the OMFP.',
        required= False
        )

    get_parser.add_argument( '-e', '--ediff', type=float, help="Filter by energy difference per atom", dest='ediff',
        required=False, default=np.inf)
    get_parser.add_argument('-n', '--nmax', type=int, help="Maximal elements of each stoichiometry",
        dest='nmax', default=np.inf, required=False)
    get_parser.add_argument('-o', '--outdir', type=str, help="Output directory will be cleaned up before use. Default is output/",
        dest='outdir', default='output', required=False) 
    get_parser.add_argument('-t', '--extension', type=str, default='extxyz', dest='ext', 
        required=False, choices=structureDB.get.allowed_extensions, help="File format of output files.")

    args = parser.parse_args()

    if args.command == 'init':
        if structureDB.initialize_db.isInitialized():
            print('Database already initialized. Quitting.')
            sys.exit(1)
        parameters = structureDB.parameters.structureDBParameters(args.ns, args.np, args.width_cutoff,
            args.maxnatsphere, args.fpd_max, args.e_thresh, args.exclude, args.name + '/')
        structureDB.initialize_db.initialize(parameters)
        sys.exit(0)
    elif not structureDB.initialize_db.isInitialized():
        print("Database must be initialized first")
        sys.exit(1)

    # database is initialized and command is not init

    if args.command == 'add':
        structureDB.add.add_files(args.files)
    if args.command == 'convexHull':
        structureDB.convexHull.calcConvexHull(args.outfilename, args.onlypositions, args.e1, args.e2, args.e3)
    if args.command == 'get':
        structureDB.get.get(args.ediff, args.nmax, args.outdir, args.ext)


