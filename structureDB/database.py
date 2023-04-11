from ase.io import read, write
import os
import structureDB.database
from ase.atoms import Atoms
import ase.formula
import bisect
import structureDB.omfp.fpd
import structureDB.parameters
import glob


def read_structure_database(database_path):
    files = find_files(database_path)
    database = {}
    for f in files:
        stoichio = filenameToStoichio(f)
        database[stoichio] = read( database_path + f, index=':')
    return database

def writeStructureDB(db, database_path):
    for st in db:
        if os.path.exists(stoichioToFilename(st, database_path)):
            os.remove(stoichioToFilename(st, database_path))
        write(stoichioToFilename(st, database_path), db[st])

def find_files(database_path):
    return os.listdir(database_path)
    # return glob.glob(database_path + '/*.extxyz')

def stoichioToFilename(stoichio: str, database_path):
    return database_path + '/' + stoichio + '.extxyz'

def filenameToStoichio(fname):
    return fname.split('.')[0]

def getStoichiometry(struct: Atoms):
    return ase.formula.Formula.from_list(struct.get_chemical_symbols()).format('hill')

def addAtoms(db: dict, atomList: list, parameters: structureDB.parameters.structureDBParameters):
    for struct in atomList:
        st = getStoichiometry(struct)
        if 'energy' not in struct.info:
            print("Energy missing: ", st)
            struct.info["energy"] = 0.0
        if st not in db:
            db[st] = [struct]
            continue
        i_start = bisect.bisect_left(db[st], struct.info['energy'], key= lambda x: x.info['energy'])

        # start backward check
        already_found = False
        i_compare = i_start - 1
        while i_compare >= 0:
            if abs(db[st][i_compare].info['energy'] - struct.info['energy']) > parameters.e_thresh:
                break
            if structureDB.omfp.fpd.calcFingerprintDistance(db[st][i_compare], struct, parameters.ns,
                parameters.np, parameters.width_cufoff, parameters.maxnatsphere, parameters.exclude) < parameters.fpd_max:
                already_found = True
                break
            i_compare -= 1
        if already_found:
            continue

        # start forward check:
        i_compare = i_start
        while i_compare < len(db[st]):
            if abs(db[st][i_compare].info['energy'] - struct.info['energy']) > parameters.e_thresh:
                break
            if structureDB.omfp.fpd.calcFingerprintDistance(db[st][i_compare], struct, parameters.ns,
                parameters.np, parameters.width_cufoff, parameters.maxnatsphere, parameters.exclude) < parameters.fpd_max:
                already_found = True
                break
            i_compare += 1
        if already_found:
            continue
        if i_start >= len(db[st]):
            db[st].append(struct)
        else:
            db[st].insert(i_start, struct)

 