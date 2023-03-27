import structureDB.database
import structureDB.parameters
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull


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
                energy1 = db[stoichio][0].info['energy'] / len(db[stoichio][0])
            elif e2 in elem_symbs:
                st2 = stoichio
                energy2 = db[stoichio][0].info['energy'] / len(db[stoichio][0])
            elif e3 in elem_symbs:
                st3 = stoichio
                energy3 = db[stoichio][0].info['energy'] / len(db[stoichio][0])
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
    c = np.zeros(len(db))
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
        etot = db[stoichio][0].info['energy']
        etot = etot - n1 * energy1 - n2 * energy2 - n3 * energy3
        etot /= len(db[stoichio][0])
        c[i] = etot
        if c[i] > 0:
            print('houston we have a problem')
        print(stoichio, etot)
    
    point = np.concatenate((pos, c[:, np.newaxis]), axis=1)
    hull = ConvexHull(point)
    print(pos[hull.vertices,:])
    
    # fig, ax = plt.subplots()
    plt.scatter(pos[:, 0], pos[:, 1], c=c, alpha=0.8)
    plt.scatter(pos[hull.vertices, 0], pos[hull.vertices, 1], marker='x', c='red')
    plt.colorbar()
    plt.plot([0, 1], [0, 0], color = 'black')
    plt.plot([0, 0.5], [0, np.sqrt(3) / 2], color = 'black')
    plt.plot([0.5, 1], [np.sqrt(3) / 2, 0], color = 'black')

    # ax.set_xlabel(r'$\Delta_i$', fontsize=15)
    # ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=15)
    # ax.set_title('Volume and percent change')

    # ax.grid(True)
    plt.tight_layout()

    plt.annotate(e1, xy=(0, 0), xytext=(0, -10), textcoords='offset points',
              color='black', ha='center', va='center')
    plt.annotate(e2, xy=(1,0), xytext=(0, -10), textcoords='offset points',
              color='black', ha='center', va='center')
    plt.annotate(e3, xy=(0.5, np.sqrt(3)/2), xytext=(0, 10), textcoords='offset points',
                color='black', ha='center', va='center')

    plt.show()

def concentrationToPos3d(c2, c3):    
    return np.array(((c3 + 2 * c2) / 2, np.sqrt(3) * c3 / 2))