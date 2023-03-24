import structureDB.database
import structureDB.parameters
from ase.io import read
import json

def add_files(files):
    f = open(structureDB.parameters.dbname)
    parameters = structureDB.parameters.structureDBParameters(**json.load(f))
    f.close()
    db = structureDB.database.read_structure_database(parameters.db_name)
    for f in files:
        print('Processing ' + f.name)
        atoms = read(f, index=':')
        structureDB.database.addAtoms(db, atoms, parameters)
    structureDB.database.writeStructureDB(db, parameters.db_name)