**RivetCalc** is a cross-platform, open source tool for writing 
engineering calculation documents.  It's implemented as a Python 
library that produces formatted calculation documents and reports 
in  UTF8, HTML and PDF file formats from plain text input.  The tool 
is designed  to improve editing, explicitness, clarity, reuse and review.
It eliminates the problem of unusable calculation inputs arising from 
incompatible binary files and programs. 

**RivetCalc** calculations are written in **rivet**, a light-weight, 
context and index based markup language. The language includes 
a dozen commands, tags, and a subset of reStructuredText that 
may be mixed arbitrarily with utf-8 text strings.

A **RivetCalc** file is a Python file that typically imports 
*rivetcalc.rc_lib as rc* and calls the API functions as e.g. 
rc.R('''**rivet-string**'''), where **rivet-string** contains 
arbitrary text and **rivet** commands and tags.

Input file names (models) have the form *rddcc_calcname.py*. Corresponding 
output files (calcs and docs) have the names *rddcc_calcname.txt*, 
*rddcc_calcname.html*, or *rddcc_calcname.pdf*; where dd (division) 
and cc (calculation) are two digit numbers used to organize PDF documents 
into collated reports. 

===================  =====================================================
File type             File description                                      
===================  =====================================================
design (.py)          text input model, written in rivet                      
calc (.txt)           formatted UTF-8 output, written to screen (and file) 
doc (.pdf or .html)   formatted HTML or PDF output, written to file                  
report (.pdf)         organized and formatted PDF docs, written to file
===================  =====================================================       

The **RivetCalc** API consists of five functions that take a **rivet** 
string as input and several functions that control output:

================ =======================================================
 API              Description
================ =======================================================
  R()            repository, report and calc summary information
  I()            insert descriptive text, tables, figures and equations
  V()            define and import values 
  E()            define and import equations and functions
  T()            define tables and plots   
list_values()    summary table of current evaluated values  
write_utfcalc()  write utf calc to file
write_pdfdoc()   write pdf doc to file (includes images)
write_htmldoc()  write html doc to file (include images) 
write_report()   compile pdf docs into a report
================ =======================================================

Any file needed for a calcuation is stored in a project folder tree.  UTF-8 calcs 
are written to the *calcs* folder. Docs are written to their respective folders 
in PDF or HTML formts. PDF reports are written to the *reports* folder. Binary  
image files used in docs and reports are stored in the *html* folder. The user 
initially creates the complete folder tree either from scratch or starting with
an existing project or template::

  Project_Name (chosen by user)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
          |- temp
      |- docs
          |- html
      |- reports
          |- attachments

Folders are restricted in the types of files they contain for the purposes of 
sharing templates and search. The *calcs* folder and sub-folders may contain only 
UTF-8 or ASCII files. Binary files, including image and PDF files, are stored in 
the *docs* and *reports* folders.

**RivetCalc** templates are full project trees with  UTF-8 *calcs* folders that
fully define a calc or set of calcs. The *docs* and *reports* folders are 
empty, except for a few default config files (needed to keep the folder 
structure intact on Github). Templates have the form::

  RivetCalcTemplate_nnnn (nnn is a unique three digit number)
      |- calcs
          |- sketches
          |- scripts
          |- tables
          |- text
          |- temp
      |- docs
          |- html
      |- reports
          |- attachments

***RivetCalcTemplate_nnnn*** is the actual Github repository 
name appended with a unique three digit number.  This common name root 
across all Github accounts and repositories facilitates searches. 
Each account may contain many repositories (templates). RivetCalc 
templates may be cloned, downloaded as a zip file, or run on Gitpod
or repl.it with the addition of a few setup files.

The minimum working version of **RivetCalc** includes a Python 
installation with a dozen Python science libraries 
(https://github.com/rivetcalcs/rivet-code/requirements.txt) 
and a text editor. In this case the input model is run from 
the command line as::

  python -m rivetcalc ddcc_calcname.py 

If a LaTeX distribution is installed, formatted PDF documents and 
reports can be generated. If an IDE or full-featured code editor 
is used the calculations can be executed interactively and in stages 
by tagging the API functions as cells. The program documentation, 
for example, focuses on the use case of **VSCode** and extensions, 
which dramatically increases calculation efficiency. Execution steps 
include::

                     /--------------------------------\                    
                     |   Edit and run RivetCalc       |
                     |   model file or cells.         |                   
                     |                                |
                     |          cell types:           |                    
                     |    R(), I(), V(), E(), T()     |                    
                     \--------------------------------/                    
                                     \/                                    
  +--------------+|  +--------------------------------+  +-------------+
  |    Process    |  |   Working in interactive IDE?  |  |  Process    |   
  |    cell or    |  |     (VSCode, Spyder, Pyzo)     |  |  file       |   
  |    file       <--+ YES                         NO +-->             |   
  +------+--------+  +--------------------------------+  +------+------+   
         |           +================================+         |          
         |           |  Write utf-8 calc to :         |         |          
         +===========>    terminal   |  file          <=========+            
                     |================================|                    
                     +================================+                    
                                     \/
                     +================================+                    
                     |   Write reST calc file if      |
                     |   complete file is processed.  |       
                     |================================|                    
                     +================================+                    
                                     \/
  +===============+  +--------------------------------+                    
  | Write HTML    |  |                                |  /---------\    
  | or PDF doc    |  |         Write docs?            |  |   End   |   
  | files         <==+ YES                         NO +==>         |   
  |===============|  +--------------------------------+  \---------/ 
  +=====+=========+        
        |            +--------------------------------+  /---------\   
        |            |         Write report?          |  |   End   |   
        +============>                             NO +==>         |   
                     +----------------+---------------+  \---------/ 
                                     \/ YES
                     +================================+                    
                     |    Write PDF report file       |                    
                     |================================|                    
                     +================================+    
                     
                     
**RivetCalc** may be installed by:

1. Locally Installing and configuring the individual open source components (a half dozen steps).
2. Locally downloading and unzipping a single no-install file for Windows (a couple of steps).
3. Remotely running a cloud service in a container (a dozen steps). 

Pre-installed cloud installations (**RivetCloud.net**) are available with paid support. 
Refer to the **RivetCalc User Manual** for details.

                               
                                                                           
                                                                          
