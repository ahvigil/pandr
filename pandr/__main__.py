import pandr
import sys

import logging
logging.basicConfig()
logging.getLogger('pandr').setLevel(logging.DEBUG)

print pandr.load(sys.argv[1])
