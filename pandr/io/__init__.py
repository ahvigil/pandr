import xdrlib
from gzip import GzipFile
from bz2 import BZ2File
import six

import pandr.io.utils
import pandr.constants.rinternals
from pandr.constants import R_XDR_INTEGER_SIZE, SIZEOF_DOUBLE, SIZEOF_INT
from pandr.sexp import SEXP, SEXPTYPE

# File format constants
XDR_FILE = 100
BINARY_FILE = 101
ASCII_FILE = 102

class RFile(six.Iterator):
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
        self._read_header()

    def read(self):
        return self.read_SEXP()

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return self.read()
        except EOFError as e:
            raise StopIteration

    def _read_header(self):
        magic = self._file.readline().strip()

        if type(magic) is bytes:
            magic = str(magic)

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
                self._version = 1
            elif '2' in magic:
                self._version = 2
            else:
                raise NotImplementedError('Unsupported file version %s' % magic)
            if self._version != 2:
                raise NotImplementedError("Only version 2 saves supported, got %d" % self._version)

            ftype = self._file.readline().strip()

        #assert ftype == 'X'
        self._version = self.read_int()
        self._rversion = "%d.%d.%d" % pandr.io.utils.decode_version(self.read_int())
        self._min_rversion = "%d.%d.%d" % pandr.io.utils.decode_version(self.read_int())

    def read_int(self):
        """
        Parse the next 4 bytes in the stream as an integer
        """
        if self._format == XDR_FILE:
            data = xdrlib.Unpacker(self._file.read(R_XDR_INTEGER_SIZE)).unpack_int()

        elif self._format == ASCII_FILE:
            data = self._file.readline().strip()
            if not data:
                raise EOFError
            data = int(data)

        return data

    def read_int_array(self):
        """
        Read a vector of integers
        """
        length = self.read_array_length()
        if self._format == XDR_FILE:
            unpacker = xdrlib.Unpacker(self._file.read(length*R_XDR_INTEGER_SIZE))
            data = unpacker.unpack_farray(length, unpacker.unpack_int)
        elif self._format == ASCII_FILE:
            data = [int(self._file.readline().strip()) for i in range(length)]

        return data

    def read_float_array(self):
        """
        Get a vector of real numbers from the input stream, assuming
        numbers are stored according to XDR double floating point standard
        """
        length = self.read_array_length()

        if self._format == XDR_FILE:
            unpacker = xdrlib.Unpacker(self._file.read(length*SIZEOF_DOUBLE))
            data = unpacker.unpack_farray(length, unpacker.unpack_double)
        else:
            data = [float(self._file.readline().strip()) for i in range(length)]

        return data

    def read_complex(stream):
        raise NotImplementedError("Complex values not yet implemented")

    def read_complex_array(stream, length):
        raise NotImplementedError("Complex values not yet implemented")

    def read_char(self, n = 1):
        """
        Get n characters from the stream and return them as a string
        """
        if n<0: return "NA"
        else: return self._file.read(n)

    def read_string(self):
        length = self.read_int()
        string = self.read_char(length)

        return string

    def read_string_array(self):
        length = self.read_int()
        data = [self.read_string() for i in range(length)]

        if length == 1:
            data = data[0]

        return data

    def read_array_length(self):
        length = self.read_int()

        # very long arrays might need 64 bits to store length
        if length is -1:
            len1 = long( self.read_int() )
            len2 = long( self.read_int() )
            length = ( len1 << 32 ) + len2

        return length

    def close(self):
        self._file.close()

    def getFlags(self):
        flags = self.read_int()
        return pandr.io.utils.unpack_flags(flags)

    def getRefIndex(self):
        """
        """
        flags = self.read_int()
        i = flags >> 8
        if i is 0:
            return self.read_int()
        else:
            return i

    def read_SEXP(self):
        expression = None
        (ptype, plevs, pisobj, phasattr, phastag) = self.getFlags();

        # numeric vectors
        if ptype == pandr.constants.rinternals.REALSXP:
            expression = self.read_REALSXP()

        # string vectors
        elif ptype == pandr.constants.rinternals.STRSXP:
            expression = self.read_STRSXP()

        # character expressions
        elif ptype == pandr.constants.rinternals.CHARSXP:
            expression = self.read_CHARSXP()

        # integer vectors
        elif ptype == pandr.constants.rinternals.INTSXP:
            expression = self.read_INTSXP()

        else:
            raise NotImplementedError('No support for {}'.format(SEXP(ptype)))

        return expression

    def read_REALSXP(self):
        """Numeric vector expression.
        """
        data = self.read_float_array()
        if len(data) == 1:
            data = data[0]
        return SEXP('REALSXP', data)

    def read_STRSXP(self):
        """Vector of strings.
        """
        length = self.read_array_length()
        data = [self.read_SEXP() for i in range(length)]
        if length == 1:
            data = data[0]
        return SEXP('STRSXP', data)

    def read_CHARSXP(self):
        """Character expression.
        """
        return SEXP('CHARSXP', self.read_string())

    def read_INTSXP(self):
        """Integer vector expression.
        """
        return SEXP('INTSXP', self.read_int_array())

    # def getExpression(self):
    #     (ptype, plevs, pisobj, phasattr, phastag) = self.getFlags();
    #
    #     sexp=None
    #     if ptype in [pandr.constants.rinternals.NILVALUE_SXP]:
    #         sexp = SEXP('NILVALUE_SXP')
    #     # Pairlist-like objects write their attributes (if any), tag (if
    #     # any), CAR and then CDR (using tail recursion)
    #     elif ptype in [pandr.constants.rinternals.LISTSXP]:
    #         sexp = SEXP('LISTSXP')
    #         if phasattr:
    #             sexp.attr = self.getExpression()
    #         if phastag:
    #             sexp.tag = self.getExpression()
    #         # CAR
    #         sexp.CAR = self.getExpression()
    #         if sexp.CAR:
    #             # CDR
    #             sexp.CDR = self.getExpression()
    #
    #     # other objects write their attributes after themselves
    #     else:
    #         if ptype in [pandr.constants.rinternals.REALSXP]:
    #             sexp = self.read_REALSXP()
    #         elif ptype in [pandr.constants.rinternals.REFSXP]:
    #             index = self.getRefIndex() - 1 # R uses base 0 indexes, need to adjust
    #         elif ptype in [pandr.constants.rinternals.INTSXP]:
    #             sexp = SEXP('INTSXP', self.read_int_array())
    #         elif ptype in [pandr.constants.rinternals.STRSXP]:
    #             length=self.read_array_length()
    #             sexp = SEXP('STRSXP', value=[self.getExpression() for i in range(length)])
    #         elif ptype in [pandr.constants.rinternals.CHARSXP]:
    #             sexp = SEXP('CHARSXP', value=self.read_string())
    #         elif ptype in [pandr.constants.rinternals.SYMSXP]:
    #             sexp = SEXP('SYMSXP', value=[self.getExpression(), self.getExpression()])
    #         elif ptype in [pandr.constants.rinternals.VECSXP]:
    #             length = self.read_array_length()
    #             sexp = SEXP('VECSXP', value=[self.getExpression() for i in range(length)])
    #
    #         if sexp:
    #             if phasattr:
    #                 sexp.attr = self.getExpression()
    #             if phastag:
    #                 sexp.tag = self.getExpression()
    #
    #     return sexp

def _open(name, mode='rb', buffering=1):
    file_object = open(name, mode, buffering)
    magic = file_object.read(3)

    # gzip
    if magic == b'\x1f\x8b\x08':
        file_object = GzipFile(name, mode, buffering)

    # bz2
    elif magic == b'BZh':
        file_object = BZ2File(name, mode, buffering)

    # xz
    elif magic == b'\xfd7z':
        raise NotImplementedError("xz compression not supported")

    else:
        file_object.seek(0)

    return file_object
