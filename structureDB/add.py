import structureDB.database
from ase.io import read

def add_files(files):
    db = structureDB.database.read_structure_database()
    for f in files:
        print('Processing ' + f.name)
        atoms = read(f, index=':')
        structureDB.database.addAtoms(db, atoms)
    structureDB.database.writeStructureDB(db)