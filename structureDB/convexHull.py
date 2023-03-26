import structureDB.database
import structureDB.parameters
import json
import numpy as np
import matplotlib.pyplot as plt


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
        if not elem_symbs.issubset({e1, e2, e3}):
            print(elem_symbs, "not given, stopping")
            quit()
        if len(elem_symbs) == 1: # single component system found
            if e1 in elem_symbs:
                st1 = stoichio
            elif e2 in elem_symbs:
                st2 = stoichio
            elif e3 in elem_symbs:
                st3 = stoichio
            else:
                print("this should not have happened.")
                quit()
    if st1 == None:
        print("Single component %s not found!"%e1)
    if st2 == None:
        print("Single component %s not found!"%e2)
    if st3 == None:
        print("Single component %s not found!"%e3)
    pos = np.zeros((len(db), 2))
    for i, stoichio in enumerate(db):
        elem_symbs = db[stoichio][0].get_chemical_symbols()
        n1 = elem_symbs.count(e1)
        n2 = elem_symbs.count(e2)
        n3 = elem_symbs.count(e3)
        n = n1 + n2 + n3
        conc_1 = n1 / n
        conc_2 = n2 / n
        conc_3 = n3 / n
        pos[i, 0] = (conc_3 + 2 * conc_2) / 2
        pos[i, 1] = np.sqrt(3) * conc_3 / 2
    
    
    fig, ax = plt.subplots()
    ax.scatter(pos[:, 0], pos[:, 1], alpha=0.5)

    plt.plot([0, 1], [0, 0], color = 'black')
    plt.plot([0, 0.5], [0, np.sqrt(3) / 2], color = 'black')
    plt.plot([0.5, 1], [np.sqrt(3) / 2, 0], color = 'black')

    # ax.set_xlabel(r'$\Delta_i$', fontsize=15)
    # ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=15)
    # ax.set_title('Volume and percent change')

    # ax.grid(True)
    fig.tight_layout()

    ax.annotate(e1, xy=(0, 0), xytext=(0, -10), textcoords='offset points',
                color='black', ha='center', va='center')
    ax.annotate(e2, xy=(1,0), xytext=(0, -10), textcoords='offset points',
                color='black', ha='center', va='center')
    ax.annotate(e3, xy=(0.5, np.sqrt(3)/2), xytext=(0, 10), textcoords='offset points',
                color='black', ha='center', va='center')

    plt.show()

def concentrationToPos3d(c2, c3):    
    return np.array(((c3 + 2 * c2) / 2, np.sqrt(3) * c3 / 2))