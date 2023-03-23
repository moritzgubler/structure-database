from ase.io import read, write
import os
import structureDB.database
from ase.atoms import Atoms
import ase.formula

database_path = "structureDB/"

def read_structure_database():
    files = find_files()

def find_files():
    return os.listdir(structureDB.database.database_path)

def getStoichiometry(struct: Atoms):
    return ase.formula.Formula.from_list(struct.get_chemical_symbols()).format('hill')