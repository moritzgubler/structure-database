from ase.io import read, write
import os
import structureDB.database
from ase.atoms import Atoms
import ase.formula

database_path = "structureDB/"

def read_structure_database():
    files = find_files()
    database = {}
    for f in files:
        stoichio = f.split('.')[0]
        database[stoichio] = read(f, index=':')
    return database

def find_files():
    return os.listdir(structureDB.database.database_path)

def getStoichiometry(struct: Atoms):
    return ase.formula.Formula.from_list(struct.get_chemical_symbols()).format('hill')

def addAtoms(atomList: list):
    for atom in atomList:
        ...