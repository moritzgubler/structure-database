import structureDB.database
from ase.io import write
import os
import shutil

allowed_extensions = ['ascii', 'extxyz', 'in']

concatanable = {
    'ascii': False,
    'extxyz': True,
    'in': False
}

def get(emax, nmax, outdir, extension):
    # delete output file or directory if present.
    if os.path.isfile(outdir) or os.path.islink(outdir):
        os.remove(outdir)
    elif os.path.isdir(outdir):
        shutil.rmtree(outdir)
    
    os.mkdir(outdir)
    db = structureDB.database.read_structure_database()
    for st in db:
        i = 0
        at_list = []
        while i < len(db[st]):
            if i >= nmax or (db[st][i].info['energy'] - db[st][0].info['energy']) / len(db[st][0]) > emax:
                break
            at_list.append(db[st][i])
            i+=1
        if concatanable[extension]:
            write(outdir + '/' + st + '.' + extension, at_list)
        else:
            for i, struct in enumerate(at_list):
                write("%s/%s_%s.%s"%(outdir, st, format(i, '05'), extension), struct)