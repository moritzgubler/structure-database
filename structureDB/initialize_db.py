import os
import structureDB.database

def initialize():
    print("Initializing databse in current working directory")
    os.mkdir(structureDB.database.database_path)


def isInitialized():
    return os.path.isdir(structureDB.database.database_path)