import pandr
import pandr.sexp
import pytest

from glob import glob

@pytest.mark.parametrize("filename", glob('tests/data/rds/x.*'))
def test_simple_rds_load(filename):
    try:
        assert pandr.load(filename) == pandr.sexp.SEXP('REALSXP', 5)
    except NotImplementedError:
        pytest.skip("Not implemented")
