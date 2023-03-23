from scipy import optimize
import numpy as np
from structureDB.omfp.OverlapMatrixFingerprint import OverlapMatrixFingerprint as OMFP
import numba
from numba import njit

def calcFingerprintDistance(struct1, struct2):
    fp1 = get_OMFP(struct1)
    fp2 = get_OMFP(struct2)
    n_dim1 = len(fp1.shape)
    n_dim2 = len(fp2.shape)

    assert n_dim1 == n_dim2, "Dimension of vector 1 is and vector 2 is different"
    assert n_dim1 < 3, "Dimension of vector 1 is larger that 2"
    assert n_dim2 < 3, "Dimension of vector 2 is larger that 2"

    if n_dim1 == 1 and n_dim2 == 1:
        fp_dist = np.linalg.norm(fp1 - fp2) / len(struct1)
    else:
        costmat = _costmatrix(fp1, fp2)
        ans_pos = optimize.linear_sum_assignment(costmat)
        # use this formula for euclidian fingerprint distance
        # fp_dist = np.linalg.norm( self.fp[ans_pos[0], :] - other.fp[ans_pos[1], :]) / len(self.atoms)
        fp_dist = np.max( np.abs(fp1[ans_pos[0], :] - fp2[ans_pos[1], :]) )

    return fp_dist

@njit
def _costmatrix(desc1, desc2):
    """
    Cost matrix of the local fingerprints for the hungarian algorithm
    """
    # assert desc1.shape[0] == desc2.shape[0], "descriptor has not the same length"

    costmat = np.zeros((desc1.shape[0], desc2.shape[0]))

    for i, vec1 in enumerate(desc1):
        for j, vec2 in enumerate(desc2):
            costmat[i, j] = np.linalg.norm(vec1 - vec2)
    return costmat


def fingerprint_distance(self, other):
    """
     Calcualtes the fingerprint distance of 2 structures with local environment descriptors using the hungarian algorithm
     if a local environment descriptor is used. Else the distance is calculated using l2-norm.
     """



def get_OMFP(atoms, s=1, p=0, width_cutoff=4, maxnatsphere=50, exclude=[]):
        """
        Calculation of the Overlapmatrix fingerprint. For peridoic systems a local environment fingerprint is calculated
        and a hungarian algorithm has to be used for the fingerprint distance. For non-periodic systems a global fingerprint
        is calculated and a simple l2-norm is sufficient for as a distance measure.

        If you use that function please reference:

        @article{sadeghi2013metrics,
        title={Metrics for measuring distances in configuration spaces},
        author={Sadeghi, Ali and Ghasemi, S Alireza and Schaefer, Bastian and Mohr, Stephan and Lill, Markus A and Goedecker, Stefan},
        journal={The Journal of chemical physics},
        volume={139},
        number={18},
        pages={184118},
        year={2013},
        publisher={American Institute of Physics}
        }

        and

        @article{zhu2016fingerprint,
        title={A fingerprint based metric for measuring similarities of crystalline structures},
        author={Zhu, Li and Amsler, Maximilian and Fuhrer, Tobias and Schaefer, Bastian and Faraji, Somayeh and Rostami, Samare and Ghasemi, S Alireza and Sadeghi, Ali and Grauzinyte, Migle and Wolverton, Chris and others},
        journal={The Journal of chemical physics},
        volume={144},
        number={3},
        pages={034203},
        year={2016},
        publisher={AIP Publishing LLC}
        }
        """

        _pbc = list(set(atoms.pbc))
        assert len(_pbc) == 1, "mixed boundary conditions"
        _ang2bohr = 1.8897161646320724

        _symbols = atoms.get_chemical_symbols()
        _positions = atoms.get_positions()
        _elements = atoms.get_atomic_numbers()
        _selected_postions = []
        _selected_elem = []

        for symb,elem, pos in zip(_symbols, _elements,_positions):
            if symb not in exclude:
                _selected_postions.append(pos)
                _selected_elem.append(elem)
        _selected_postions = np.array(_selected_postions)


        if True in _pbc:
            _selected_positions = _selected_postions*_ang2bohr
            _lattice = atoms.get_cell()*_ang2bohr
            _omfpCalculator = OMFP.stefansOMFP(s=s, p=p, width_cutoff=width_cutoff, maxnatsphere=maxnatsphere)
            _omfp = _omfpCalculator.fingerprint(_selected_positions, _selected_elem, lat=_lattice)
            _omfp = np.array(_omfp)

        else:
            _selected_positions = _selected_postions*_ang2bohr
            _elements = atoms.get_atomic_numbers()
            # _width_cutoff = 1000000
            _maxnatsphere = len(atoms)
            _omfpCalculator = OMFP.stefansOMFP(s=s, p=p, width_cutoff=width_cutoff, maxnatsphere=_maxnatsphere)
            # _omfp = _omfpCalculator.globalFingerprint(_selected_positions, _selected_elem)
            _omfp = _omfpCalculator.fingerprint(_selected_positions, _selected_elem)
            _omfp = np.array(_omfp)
        return _omfp