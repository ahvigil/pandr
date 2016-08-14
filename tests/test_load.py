import pandr
import pandr.sexp
import pytest

from glob import glob

@pytest.mark.parametrize("filename,expected",
    [(f, 5) for f in glob('tests/data/types/integer.*')] +
    [(f, 'test123') for f in glob('tests/data/types/string.*')] +
    [(f, [1,2,3,4,5]) for f in glob('tests/data/types/integer_vec.*')]
)
def test_simple_rds_load(filename, expected):
    try:
        assert pandr.load(filename) == expected
    except NotImplementedError:
        pytest.skip("Not implemented")
