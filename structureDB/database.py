from ase.io import read, write
import os
import structureDB.database
from ase.atoms import Atoms
import ase.formula
import bisect
import structureDB.omfp.fpd

database_path = "structureDB/"
fp_cutoff = 0.05
e_cutoff = 0.001

def read_structure_database():
    files = find_files(database_path)
    database = {}
    for f in files:
        stoichio = filenameToStoichio(f)
        database[stoichio] = read(f, index=':')
    return database

def find_files():
    return os.listdir(structureDB.database.database_path)

def stoichioToFilename(stoichio: str):
    return database_path + stoichio + '.extxyz'

def filenameToStoichio(fname):
    return fname.split('.')[0]

def getStoichiometry(struct: Atoms):
    return ase.formula.Formula.from_list(struct.get_chemical_symbols()).format('hill')

def addAtoms(atomList: list):
    db = read_structure_database(database_path)
    for struct in atomList:
        st = getStoichiometry(struct)
        if st not in db:
            db[st] = [struct]
            continue
        i_start = bisect.bisect_left(db[st], struct, key= lambda x: x.info['energy'])

        # start backward check
        already_found = False
        i_compare = i_start - 1
        while i_compare >= 0:
            if abs(db[st][i_compare].info['energy'] - struct.info['energy']) > e_cutoff:
                break
            if structureDB.omfp.fpd.calcFingerprintDistance(db[st][i_compare], struct) < fp_cutoff:
                already_found = True
                break
            i_compare -= 1
        if already_found:
            continue

        # start forward check:
        i_compare = i_start
        while i_compare < len(db[st]):
            if abs(db[st][i_compare].info['energy'] - struct.info['energy']) > e_cutoff:
                break
            if structureDB.omfp.fpd.calcFingerprintDistance(db[st][i_compare], struct) < fp_cutoff:
                already_found = True
                break
            i_compare += 1
        if already_found:
            continue
    if i_start >= len(db[st]):
        db[st].append(struct)
    else:
        db[st].insert(i_start, struct)
    os.remove(stoichioToFilename(st))
    write(stoichioToFilename(st), db[st])
        