import structureDB.database
import structureDB.parameters
import json

def calcConvexHull(outfile: str, plotOnly: bool, e1: str, e2: str, e3: str):
    print('Calculating convex hull in conv hull')
    f = open(structureDB.parameters.dbname)
    parameters = structureDB.parameters.structureDBParameters(**json.load(f))
    f.close()
    db = structureDB.database.read_structure_database(parameters.db_name)
    st1 = None
    st2 = None
    st3 = None
    # get single component systems:
    for stoichio in db:
        elem_symbs = set(db[stoichio][0].get_chemical_symbols())
        if e1 not in elem_symbs or e2 not in elem_symbs or e3 not in elem_symbs:
            print(elem_symbs, "not given, stopping")
            quit()
        if len(elem_symbs) == 1: # single component system found
            if elem_symbs[0] == e1:
                st1 = stoichio
            elif elem_symbs[0] == e2:
                st2 = stoichio
            elif elem_symbs[0] == e3:
                st3 = stoichio
            else:
                print("this should not have happened.")
                quit()
    
    for stoichio in db:
        elem_symbs = db[stoichio][0].get_chemical_symbols()
        n1 = elem_symbs.count(e1)
        n2 = elem_symbs.count(e2)
        n3 = elem_symbs.count(e3)