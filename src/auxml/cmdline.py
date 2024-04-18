import argparse
import logging
import sys

class CmdLine:
    already_initialized = False
    
    def __init__(self):
        if CmdLine.already_initialized:
            raise Exception("CmdLine object already initialized")
        self.args = {}
        self.parse_arguments()

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description="Your script description here.")

        parser.add_argument('--macros', required=True, help='specify the input macro XML file')
        parser.add_argument('--infile', required=True, help='specify the input XML file')
        parser.add_argument('--outfile', required=True, help='specify output file')
       
        parser.add_argument(
            "-v",
            "--verbose",
            dest="loglevel",
            help="set loglevel to INFO",
            action="store_const",
            const=logging.INFO,
        )
        
        parser.add_argument(
            "-vv",
            "--very-verbose",
            dest="loglevel",
            help="set loglevel to DEBUG",
            action="store_const",
            const=logging.DEBUG,
        )
        
        # Parse the command-line arguments
        self.args = parser.parse_args()
        self.setup_logging(self.args.loglevel)
        CmdLine.already_initialized = True

    def setup_logging(self, loglevel):
        logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
        logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

    def infile(self):
        return self.args.infile
    
    def macros(self):
        return self.args.macros
        
    def outfile(self):
        return self.args.outfile
    
    
cmdline = CmdLine()

