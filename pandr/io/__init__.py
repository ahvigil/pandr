import xdrlib
from gzip import GzipFile
from bz2 import BZ2File

import pandr.io.utils
import pandr.constants.rinternals
from pandr.constants import R_XDR_INTEGER_SIZE, SIZEOF_DOUBLE, SIZEOF_INT

# File format constants
XDR_FILE = 100
BINARY_FILE = 101
ASCII_FILE = 102

class RFile(object):
    """
    """
    def __init__(self, name, mode='rb', buffering=1):
        self._file=None
        self._format=None
        self._rdata=None
        # file version info
        self._version = None
        self._rversion = None
        self._min_rversion = None

        self._file = _open(name, mode, buffering)
        self.readHeader()

    # read n bytes from file
    def read(self):
        return self.next()

    def __iter__(self):
        return self

    def next(self):
        try:
            ptype, plevs, pisobj, phasattr, phastag = self.getFlags()
            if ptype == pandr.constants.rinternals.REALSXP:
                return self.getRealVec()
            else:
                return NotImplementedError('No support for SEXP type %s' % ptype)
        except EOFError:
            raise StopIteration

    # Read header for format and file version
    def readHeader(self):
        magic = self._file.readline().strip()

        if 'A' in magic:
            self._format = ASCII_FILE
        elif 'B' in magic:
            self._format = BINARY_FILE
        elif 'X' in magic:
            self._format = XDR_FILE
        else:
            raise NotImplementedError('Unsupported file version %s' % magic)

        if 'RD' in magic:
            self._rdata = True
            if '1' in magic:
                self.__version = 1
            elif '2' in magic:
                self.__version = 2
            else:
                raise NotImplementedError('Unsupported file version %s' % magic)
            if self._version is not 2:
                raise NotImplementedError("Only version 2 saves supported")

            ftype = self._file.readline().strip()

            raise NotImplementedError('RData files not yet implemented')

        #assert ftype == 'X'
        self._version = self.getInteger()
        self._rversion = "%d.%d.%d" % pandr.io.utils.decode_version(self.getInteger())
        self._min_rversion = "%d.%d.%d" % pandr.io.utils.decode_version(self.getInteger())

    def close(self):
        self._file.close()

    def getLength(self):
        length = self.getInteger()

        # very long arrays might need 64 bits to store length
        if length is -1:
            len1 = long( self.getInteger() )
            len2 = long( self.getInteger() )
            length = ( len1 << 32 ) + len2

        return length

    def getInteger(self):
        """
        Parse the next 4 bytes in the stream as an integer
        """
        if self._format == XDR_FILE:
            return xdrlib.Unpacker(self._file.read(R_XDR_INTEGER_SIZE)).unpack_int()
        elif self._format == ASCII_FILE:
            data = self._file.readline().strip()
            if not data:
                raise EOFError
            return int(data)

    def getFlags(self):
        flags = self.getInteger()
        return pandr.io.utils.unpack_flags(flags)

    def getRefIndex(self):
        """
        """
        flags = self.getInteger()
        i = flags >> 8
        if i is 0:
            return self.getInteger()
        else:
            return i

    def getIntegerVec(self):
        """
        Read a vector of integers
        """
        length = self.getLength()
        unpacker = xdrlib.Unpacker(self.read(length*R_XDR_INTEGER_SIZE))
        data = unpacker.unpack_farray(length, unpacker.unpack_int)

        return data

    def getRealVec(self):
        """
        Get a vector of real numbers from the input stream, assuming
        numbers are stored according to XDR double floating point standard
        """
        length = self.getLength()

        if self._format == XDR_FILE:
            unpacker = xdrlib.Unpacker(self._file.read(length*SIZEOF_DOUBLE))
            data = unpacker.unpack_farray(length, unpacker.unpack_double)
        else:
            data = [float(self._file.readline().strip()) for i in range(length)]
        return data

    def getComplex(stream):
        raise NotImplementedError("Complex values not yet implemented")

    def getComplexVec(stream, length):
        raise NotImplementedError("Complex values not yet implemented")

    def getChar(self, n = 1):
        """
        Get n characters from the stream and return them as a string
        """
        if n<0: return "NA"
        else: return self._file.read(n)

    def getString(self):
        length = self.getInteger() # null terminated strings
        string = self.getChar(length)

        return string

    def getExpression(self):
        (ptype, plevs, pisobj, phasattr, phastag) = self.getFlags();

        if ptype in [NILVALUE_SXP]:
            return False

        # Pairlist-like objects write their attributes (if any), tag (if
        # any), CAR and then CDR (using tail recursion)
        if ptype in [LISTSXP]:
            if phasattr:
                self.getExpression()
            if phastag:
                self.getExpression()
            # CAR
            if not self.getExpression():
                return
            # CDR
            self.getExpression()

        # other objects write their attributes after themselves
        else:
            if ptype in [REALSXP]:
                self.getRealVec()
            elif ptype in [REFSXP]:
                index = self.getRefIndex() - 1 # R uses base 0 indexes, need to adjust
            elif ptype in [INTSXP]:
                self.getIntegerVec()
            elif ptype in [STRSXP]:
                length=self.getLength()
                for i in range(length):
                    self.getExpression()
            elif ptype in [CHARSXP]:
                self.getString()
            elif ptype in [SYMSXP]:
                self.getExpression()
                self.getExpression()
            elif ptype in [VECSXP]:
                length = self.getLength()
                for i in range(length):
                    self.getExpression()

            if phasattr:
                self.getExpression()
            if phastag:
                self.getExpression()

        return True


def _open(*args, **kwargs):
    file_object = open(*args, **kwargs)
    magic = file_object.read(3)

    # gzip
    if magic[0] == '\x1f' and magic[1] == '\x8b' and magic[2] == '\x08':
        file_object = GzipFile(*args, **kwargs)

    # bz2
    elif magic[0]=='\x42' and magic[1]=='\x5a' and magic[2]=='\x68':
        file_object = BZ2File(*args, **kwargs)

    # xz
    elif magic[0]=='\xfd' and magic[1]=='\x37' and magic[2]=='\x7a':
        raise NotImplementedError("xz compression not supported")

    else:
        file_object.seek(0)

    return file_object
