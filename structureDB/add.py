import structureDB.database
from ase.io import read, write

def add_files(files):
    for f in files:
        atoms = read(f, index=':')
        structureDB.database.addAtoms(atoms)