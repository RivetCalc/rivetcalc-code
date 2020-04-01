#! python
"""Exposes rivet-string functions.

    **rivet** markup is used in the five string functions and 4 processing
    functions exposed in this module. rivet-strings may include any unicode
    (UF-8). The first line of each string is a description. Each string type
    includes a set of commands (lines begin with ||) and tags (bracketed with
    []_). The strings may also include reStructuredText markup (
    https://docutils.sourceforge.io/docs/user/rst/quickref.html ).

    String functions and commands (see rivet_calc.py for parameter docs)
    -------------------------------------------------------------------
    r__('''r-string''') : repository and calc data 
        || summary          : summary paragraph and table of contents
        || labels           : labels for search
        || append           : append pdf files
    i__('''i-string''') : insert text and images
        || tex              : LaTeX equation
        || sym              : sympy equation
        || table            : insert table from file or inline
        || image            : insert image from file
        || image2           : insert side by side images from files
    v__('''v-string''') : define values        
        || values           : value assignments
    e__('''e-string''') : define equations
        || format           : equation format parameters
        || function         : function from file   
    t__('''t-string''') : define tables and plots
        || data             : define new table
        || write            : write table data to csv file
        || read             : read table data from csv file
        || table            : insert table from csv file
        || plot             : define new plot for table
        || add              : add data to plot from table
        || save             : write plot image to file
        || image            : insert image from file
        || image2           : insert side by side images from files

    Tags for all string functions
    ----------------------------
        [abc123]_           : citation        
        [#]_                : footnote
        [cite]_             : citation description    
        [foot]_             : footnote description
        [link]_             : http link
        [page]_             : new doc page
        [line]_             : draw horizontal line
        [r]_                : right justify line
        [c]_                : center line
        [re]_               : right justify line with equation number   

    Output functions
    ----------------
        write_values()     : write all value assignments to python file
        write_calc()       : write calc to utf8 text file
        write_pdf()        : write calc to pdf file
        write_html()       : write calc to html file
        write_report()     : write calcs to pdf report file
"""
import __main__
import os
import sys
import textwrap
import logging
import numpy
from pathlib import Path
from collections import deque
from typing import List, Set, Dict, Tuple, Optional
from tabulate import tabulate
from rivet.rivet_unit import *
import rivet.rivet_calc as _rivcalc
#import rivet.rivet_doc as _rdoc
#import rivet.rivet_reprt as _reprt
#import rivet.rivet_chk as _rchk

__version__ = "0.9.0"
__author__ = "rholland@structurelabs.com"
if sys.version_info < (3, 7):
    sys.exit("rivet requires Python version 3.7 or later")

_rivetD: dict ={}                                   # runtime dictionary
_exportL: list = []                                 # values
_utfcalcS = """"""                                  # calc print string
_rfull = Path(__main__.__file__)                    # calc file path
_rfile = Path(__main__.__file__).name               # calc file name
_rname = _rfile.split(".py")[0]                     # calc file basename
_rivpath = Path("rivet.rivet_lib.py").parent        # rivet program path
_cpath =  Path(_rfull).parent                       # calc folder path
_ppath = Path(_rfull).parent.parent                 # project folder path
_dpath = Path(_ppath / "docs")                      # doc folder path
_rpath = Path(_ppath / "reports")                   # report folder path
_txtfile = Path(_cpath / ".".join((_rname, "txt"))) # calc output
_expfile = Path(_cpath / "scripts" / "".join(("v", _rfile))) # export values

# folders 
_foldD: dict = {
"ppath": _ppath,
"cpath": Path(_rfull).parent,
"dpath": _dpath,
"rpath": _rpath,   
"spath": Path(_cpath, "scripts"),
"kpath": Path(_cpath, "sketches"),
"tpath": Path(_cpath, "tables"),
"xpath": Path(_cpath, "text"),
"hpath": Path(_dpath, "html"),
"fpath": Path(_dpath, "html/figures"),
"apath": Path(_rpath, "append"),
"mpath": Path(_rpath, "temp")
}

_rbak = Path(_foldD["mpath"] / ".".join((_rname, "bak")))
_logfile = Path(_foldD["mpath"] / ".".join((_rname, "log")))

# section settings
_setsectD: dict = {"rnum": _rname[0:4],"divnum": _rname[0:2],"calcnum": _rname[2:4],
"sectnum": 0, "sectname": "", "swidth": 80,
"eqnum":  0, "fignum": 0, "tablenum" : 0,
"footnum": 0,"footnote": 0,"footqueL": deque([1])
}

# command settings
_setcmdD = {"cwidth": 50, "scale1": 1., "scale2": 1., 
            "prec": 2, "trim": 2, "replace": False, "code": False}

# string of values for export to file
_exportS = """"""       

def shorten_path(file_path: str, length: int)-> str:
    """split path and return path of depth = length
    
    Args:
        file_path (str): path to shorten
        length (int): path depth
    
    Returns:
        str: shortened path
    """
    return Path(*Path(file_path).parts[-length:])

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=_logfile,
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

_rshort = shorten_path(_rfull, 3)
logging.info(f"""rivet file : {_rshort}""" )
with open(_rfull, "r") as f2: calcbak = f2.read()
with open(_rbak, "w") as f3: f3.write(calcbak)  # write backup
_rshort = shorten_path(_rbak, 4)
logging.info(f"""backup file written : {_rshort}""")

# todo: check folder structure here

def _update(hdrS:str):
    """update section setting dictionary
    
    Args:
        hdrs {str}: rivet-string header
    """
    global _utfcalcS, _setsectD, _rivetD

    _setsectD["eqnum"] = 0 
    _setsectD["fignum"] = 0
    _setsectD["tablenum"] = 0
    swidthI = int(_setsectD["swidth"])
    rnumS = str(_setsectD["rnum"])
    snameS = _setsectD["sectname"] = hdrS[hdrS.find("]_") + 2:].strip()
    snumS = _setsectD["sectnum"] = hdrS[hdrS.find("[")+2:hdrS.find("]_")]
    sheadS = " " +  snameS + (rnumS + " - " +
           ("[" + str(snumS) + "]")).rjust(swidthI - len(snameS) - 2)
    sstrS = swidthI * "="
    _utfcalcS += sstrS + "\n" + sheadS + "\n" + sstrS +"\n"

def r__(rawstrS: str):
    """convert repo-string to utf or rst-string
    
    Args:
        rawstrS (str): repo-string
    """
    global  _utfcalcS, _setsectD, _rivetD
    
    sectS,strS = rawstrS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    rcalc = _rivcalc._R_utf(strL, _foldD, _setsectD) 
    rcalcS, _setsectD = rcalc.r_parse()
    _utfcalcS = _utfcalcS + rcalcS

def i__(rawstrS: str):
    """convert insert-string to utf or rst-string
    
    Args:
        rawstrS (str): insert-string
    """
    global _utfcalcS, _setsectD, _foldD, _setcmdD

    sectS,strS = rawstrS.split("\n",1)
    if "]_" in sectS: _update(sectS)

    strL = strS.split("\n")
    icalc = _rivcalc._I_utf(strL, _foldD, _setcmdD, _setsectD) 
    icalcS, _setsectD, _setcmdD = icalc.i_parse()
    _utfcalcS = _utfcalcS + icalcS

def v__(rawstrS: str):
    """convert value-string to utf or rst-string
    
    Args:
        rawstr (str): value-string
    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawstrS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    vcalc = _rivcalc._V_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    vcalcS, _setsectD, _rivetD, _exportS = vcalc.v_parse()
    _utfcalcS = _utfcalcS + vcalcS

def e__(rawstrS: str):
    """convert equation-string to utf or rst-string

    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD, _exportS

    sectS,strS = rawstrS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    ecalc = _rivcalc._E_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD, _exportS)
    ecalcS, _setsectD, _rivetD, _exportS = ecalc.e_parse()
    _utfcalcS = _utfcalcS + ecalcS

def t__(rawstrS: str):
    """convert table-string to utf or rst-string
    
    """
    global _utfcalcS, _setsectD, _foldD, _rivetD, _setcmdD

    sectS,strS = rawstrS.split("\n",1)
    if "]_" in sectS: _update(sectS)
    
    strL = strS.split("\n")
    tcalc = _rivcalc._T_utf(strL, _foldD, _setcmdD, _setsectD, _rivetD)
    tcalcS, _setsectD, _rivetD = tcalc.t_parse()
    _utfcalcS = _utfcalcS + tcalcS

def x__(str0: str):
    """skip execution of a rivet-string
    """
    pass

def list_values():
    """write table of values to terminal 
    """
        
    rivetL = [[k,v] for k,v in _rivetD.items()]
    for i in rivetL:
        if isinstance(i[1], list):
            if len(i[1]) > 3:
                i[1] = i[1][0:4] + ["..."]
            else:
                pass
        if isinstance(i[1], numpy.ndarray):
            if numpy.size(i[1]) > 3:
                i[1] = numpy.hstack([i[1][:4],["..."]])
            else:
                pass    
    print("." * _setsectD["swidth"])
    print("All Defined Variables")
    print("." * _setsectD["swidth"])                
    print(tabulate(rivetL, tablefmt="grid", headers=["variable", "value"]))
    print("." * _setsectD["swidth"] + "\n")

def write_values():
    """ export calculation value assignments to Python file
 
        The file may be used for importing output from other
        rivet calcs. File name is the calc file name 
        prepended with 'v'.      
    """
    
    str1 =  ("""\nThis file contains values
            from the rivet design file 
            for lsti in zip(vlistx, vlisty)
            if __name__ == "__main__":\n
            vlist()\n\n""")
    str1 = str1 + _exportS
    with open(_expfile, 'w') as expF:
        expF.write(str1)

def utfcalc(utfcalc, _txtfile):
    """write utf calc string to file
    """
    with open(_txtfile, "wb") as f1:
        f1.write(_utfcalcS.encode("UTF-8"))

def htmldoc():
    """[summary]
    """
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def pdfdoc():
    with open(_txtfile, "wb") as f1:
        f1.write(utfcalc.encode("UTF-8"))

def pdfreport():
    """[summary]
    """
    pass

def _rstcalc(pline, pp, indent):
    """[summary]
    
    Args:
        pline ([type]): [description]
        pp ([type]): [description]
        indent ([type]): [description]
    """
    pdf_files = {
        "cpdf":  ".".join((_rbase, "pdf")),
        "chtml":  ".".join((_rbase, "html")),
        "trst":  ".".join((_rbase, "rst")),    
        "ttex1":  ".".join((_rbase, "tex")),
        "auxfile": ".".join((_rbase, ".aux")),
        "outfile":  ".".join((_rbase, ".out")),
        "texmak2":  ".".join((_rbase, ".fls")),
        "texmak3":  ".".join((_rbase, ".fdb_latexmk"))
    }
