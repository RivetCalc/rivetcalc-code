"""
***rivtCalc** may be run interactively, one cell (#%%) or function at a time
in an IDE, or from command line. If run as a command line file: 

    python -m rivtcalc rddcc_modelfile.py 

Where ddcc are division and calc numbers used for document organization. Calc
and doc output files are only generated when specified and after the file is
run, but not when used interactively.

"""
import os
import sys
import textwrap
import logging
import warnings
import re
import importlib
import numpy as np
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional

import rivtcalc.rc_lib as rc
import rivtcalc.rc_calc as _rc_calc

__version__ = "0.8.1-beta.1"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivtCalc requires Python version 3.7 or later")     

def _cmdlinehelp():
    """command line help """
    print()
    print("Run rivtCalc at the command line in the 'calc' folder with:")
    print("     python  -m rivtcalc rddcc_modelfile.py")
    print("where rddcc_ calcname.py is the model file in the folder")
    print("and **ddcc** is the model number")
    print()
    print("Specified output is written to the 'calc' or 'doc' folder:")
    print("     ddcc_userdescrip.txt")
    print("     ddcc_userdescrip.html")
    print("     ddcc_userdescrip.pdf")
    print("Logs and other intermediate files are written to the temp subfolder.")
    print()
    print("Program and documentation are here: http://rivtcalc.github.io.")
    sys.exit()

_modfileS = "empty"
if __name__ == "__main__":
    try:
        _modfileS = sys.argv[1]                       # model file argument
        _cwdS = os.getcwd()
        _cfull = Path(_modfileS)                      # model file full path
        _cfileS = Path(_cfull).name                   # calc file name
        _cname  = _cfileS.split(".py")[0]             # calc file basename
        print("current folder: ", os.getcwd())
        print("model name: ", _cfileS)
        importlib.import_module(_cname)
    except ImportError as error:
        print("error---------------------------------------------")
        print(error)
    except Exception as exception:
        # Output unexpected Exceptions.
        print("exception-----------------------------------------")
        print(exception)


