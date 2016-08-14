import os
import sys
from glob import glob

import gzip
import bz2

from six import PY3

import pandr.io

def test_file_type():
    """Test pandr.io._open returns a file like object matching the file type.
    """
    test_files = glob('tests/data/*/*')

    assert len(test_files) > 0

    for test_file in test_files:
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

def test_file_parity():
    """Test pandr.io.RFile returns same results when reading same data in different formats.
    """
    xdr = pandr.io.RFile('tests/data/rds/x.bin')
    txt = pandr.io.RFile('tests/data/rds/x.txt')

    for (x, t) in zip(xdr, txt):
        assert x==t
