"""auxml.

Usage:
  auxml [-i INFILE] [-d BUILD_DIR] [-m MACRO_FILES]...
  auxml (-h | --help)
  auxml -v

Options:
  -h --help       Show this screen.
  -v              Show version.
  -i --infile     The main input HTML file (required).
  -d --build-dir  Specify an output build directory.
  -m --macros     A list of macro files.
"""

import os
from docopt import docopt
import logging
import sys


class CmdLine():
    
    def __init__(self):
        self.args = docopt(__doc__, version="auxml 1.0")
        
        self.infile = self.args["INFILE"]
        self.macro_files = self.args["MACRO_FILES"]
        self.build_dir = self.args["BUILD_DIR"]        
        self.check()
        
    def check(self):
        print(f'     infile is : {self.infile}')
        print(f'macrofiles are : {self.macro_files}')
        print(f'  build_dir is : {self.build_dir}')
        
cmdline = CmdLine()

