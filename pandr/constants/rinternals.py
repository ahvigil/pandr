# Expression constants from Rinternals.h
NILSXP	     = 0	  # nil = NULL
SYMSXP	     = 1	  # symbols
LISTSXP	     = 2	  # lists of dotted pairs
CLOSXP	     = 3	  # closures
ENVSXP	     = 4	  # environments
PROMSXP	     = 5	  # promises: [un]evaluated closure arguments
LANGSXP	     = 6	  # language constructs (special lists)
SPECIALSXP   = 7	  # special forms
BUILTINSXP   = 8	  # builtin non-special forms
CHARSXP	     = 9	  # "scalar" string type (internal only)
LGLSXP	     = 10	  # logical vectors
# 11 and 12 were factors and ordered factors in the 1990s
INTSXP	     = 13	  # integer vectors
REALSXP	     = 14	  # real variables
CPLXSXP	     = 15	  # complex variables
STRSXP	     = 16	  # string vectors
DOTSXP	     = 17	  # dot-dot-dot object
ANYSXP	     = 18	  # make "any" args work.
#			     Used in specifying types for symbol
#			     registration to mean anything is okay
VECSXP	     = 19	  # generic vectors
EXPRSXP	     = 20	  # expressions vectors
BCODESXP     = 21     # byte code
EXTPTRSXP    = 22     # external pointer
WEAKREFSXP   = 23     # weak reference
RAWSXP       = 24     # raw bytes
S4SXP        = 25     # S4, non-vector

# used for detecting PROTECT issues in memory.c
NEWSXP       = 30    # fresh node creaed in new page
FREESXP      = 31    # node released by GC
FUNSXP       = 99    # Closure or Builtin or Special

# Special values
REFSXP            = 255
NILVALUE_SXP      = 254
GLOBALENV_SXP     = 253
UNBOUNDVALUE_SXP  = 252
MISSINGARG_SXP    = 251
BASENAMESPACE_SXP = 250
NAMESPACESXP      = 249
PACKAGESXP        = 248
PERSISTSXP        = 247
CLASSREFSXP       = 246
GENERICREFSXP     = 245
BCREPDEF          = 244
BCREPREF          = 243
EMPTYENV_SXP      = 242
BASEENV_SXP       = 241

def lookup(constant):
    """Translate between constant name and value.
    """
    env = globals()
    if type(constant) is int:
        return filter(lambda x: x[1]==constant, env.items())[0][0]
    else:
        return  filter(lambda x: x[0]==constant, env.items())[0][1]
