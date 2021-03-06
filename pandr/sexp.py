import pandr.constants.rinternals

class SEXP(object):
    def __init__(self, sexprtype, CAR=None):
        self._type = SEXPTYPE(sexprtype)
        self.CAR = CAR
        self.CDR = None
        self.tag = None
        self.attr = None

    def __eq__(self, other):
        return (self._type == other._type and
                self.CAR == other.CAR and
                self.tag == other.tag and
                self.attr == other.attr)

    def __repr__(self):
        return '{}: {}'.format(
            self._type,
            self.CAR
        )

    @property
    def value(self):
        v = self.CAR
        while isinstance(v, SEXP):
            v = v.CAR
        return v

class SEXPTYPE(object):
    def __init__(self, sexprtype):
        if type(sexprtype) is not int:
            self._constant = getattr(pandr.constants.rinternals, sexprtype)
        else:
            self._constant = sexprtype

    @property
    def name(self):
        return pandr.constants.rinternals.lookup(self._constant)

    def __repr__(self):
        return '<{}>'.format(self.name)

    def __eq__(self, other):
        return self._constant == other._constant

class SEXPFLAGS(object):
    """A collection of S Expression flags
    SEXPTYPE - The S expression type
    PLEVS - ?????
    OBJECTBIT - Is this expression an object?
    HASATTR - Does this expression have attribute data?
    HASTAG - Does this expression have a tag?
    """
    def __init__(self):
        self.type = None
        self.object = False
        self.hasattr = False
        self.hastag = False
