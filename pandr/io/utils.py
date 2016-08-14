def decode_version(packed):
    """Decode packed R version number into a human readable format.
    """
    v = packed // 65536
    packed %= 65536
    p = packed // 256
    packed %= 256
    s = packed
    return (v, p, s)

def unpack_flags(flags):
    """Decode R flags packed into the first 12 bits of a serialized object.

    Parse and return SEXP flags as in Serialize.c:UnpackFlags
    Takes in an integer containing object flags
    Returns a list of 5 items:
        SEXPTYPE - The S expression type
        PLEVS - ?????
        OBJECTBIT - Is this expression an object?
        HASATTR - Does this expression have attribute data?
        HASTAG - Does this expression have a tag?

    From the Rinternals docs:
        For all SEXPTYPEs except NILSXP, SYMSXP and ENVSXP serialization starts
        with an integer with the SEXPTYPE in bits 0:7 followed by the object bit,
        two bits indicating if there are any attributes and if there is a tag (for
        the pairlist types), an unused bit and then the gp field in bits 12:27
    """
    # set flags from bits 8-10
    pisobj = True if flags & (1 << 8) else False
    phasattr = True if flags & (1 << 9) else False
    phastag = True if flags & (1 << 10) else False

    ptype = flags & 255     # 255 ==  0000 1111 1111
    plevs = flags >> 12

    return (ptype, plevs, pisobj, phasattr, phastag)
