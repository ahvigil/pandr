import pytest
from glob import glob

import gzip
import bz2

from six import PY3

import pandr.io
import pandr.sexp

@pytest.mark.parametrize("test_file", glob('tests/data/*/*'))
def test_file_type(test_file):
    """Test pandr.io._open returns a file like object matching the file type.
    """
    try:
        f = pandr.io._open(test_file)
    except NotImplementedError:
        assert test_file.endswith('xz') # xz compression not currently supported

    if test_file.endswith('bin'):
        if PY3:
            from io import BufferedReader
            assert isinstance(f, BufferedReader)
        else:
            assert isinstance(f, file)
    elif test_file.endswith('gzip'):
        assert isinstance(f, gzip.GzipFile)
    elif test_file.endswith('bz2'):
        assert isinstance(f, bz2.BZ2File)

@pytest.mark.parametrize("xdr_file,txt_file", [
    ('tests/data/types/{0}.bin'.format(x), 'tests/data/types/{0}.txt'.format(x))
    for x in ['integer_vec', 'numeric']
])
def test_rds_file_parity(xdr_file, txt_file):
    """Test pandr.io.RFile returns same results when reading same data in different formats.
    """
    xdr = pandr.io.RFile(xdr_file)
    txt = pandr.io.RFile(txt_file)

    for (x, t) in zip(xdr, txt):
        assert x==t

@pytest.mark.parametrize("test_file", glob('tests/data/types/*'))
def test_basic_types(test_file):
    try:
        f = pandr.io.RFile(test_file)
        data = f.read_SEXP()
        assert type(data) is pandr.sexp.SEXP
    except NotImplementedError:
        pytest.skip("Not implemented")
