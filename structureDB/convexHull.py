import structureDB.database
import structureDB.parameters
import json

def calcConvexHull(outfile: str, plotOnly: bool, e1: str, e2: str, e3: str):
    print('Calculating convex hull in conv hull')
    f = open(structureDB.parameters.dbname)
    parameters = structureDB.parameters.structureDBParameters(**json.load(f))
    f.close()
    db = structureDB.database.read_structure_database(parameters.db_name)
