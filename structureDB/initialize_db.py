import os
import structureDB.database
import structureDB.parameters
import json
import sys

def initialize(parameters: structureDB.parameters.structureDBParameters):
    print("Initializing databse in current working directory")
    os.mkdir(parameters.db_name)
    f = open(structureDB.parameters.dbname, "w")
    json.dump(parameters.to_dict(), f)


def isInitialized():
    file = os.path.isfile(structureDB.parameters.dbname)
    if not file:
        return False
    f = open(structureDB.parameters.dbname)
    parameters = structureDB.parameters.structureDBParameters(**json.load(f))
    f.close()
    dir = os.path.isdir(parameters.db_name)

    if dir and file:
        return True
    if not dir and not file:
        return False
    print("Either database directory or database parameter file is missing, aborting...")
    sys.exit(1)