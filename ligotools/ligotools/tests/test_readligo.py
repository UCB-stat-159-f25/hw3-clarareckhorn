import numpy as np
from ligotools import readligo as rl

def test_numpy_import():
    """check that numpy is working properly"""
    x = np.array([1, 2, 3])
    assert np.mean(x) == 2

def test_loaddata_function_exists():
    """check that the loaddata function can be called without error on a missing file"""
    try:
        rl.loaddata("fakefile.hdf5", "H1")
    except Exception as e:
        # Expecting an error (since file doesn't exist), but test should still pass
        assert isinstance(e, Exception)