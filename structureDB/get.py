import structureDB.database
from ase.io import write

def get(emax, nmax, outdir, extension):
    db = structureDB.database.read_structure_database()
