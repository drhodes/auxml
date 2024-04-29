import os
import argparse
import logging
import sys


HELPMSG = '''

Usage: there are two ways to invoke auxml

auxml singlefile [OPTION]
auxml backend    [OPTION]

--
SUBCOMMAND: singlefile

This takes an XML infile and an XML macro definition file and expands
any macros found in the infile then writes the result to an
outfile. for example:

$ auxml singlefile --infile foo.xml --macros foo.xml --outfile bar.xml

 or more succinctly:
$ auxml singlefile -i foo.xml -m foo.xml -o bar.xml

--
SUBCOMMAND: backend

This takes four required arguments, as above --infile and --macros,
and two others: --build-type and --build-dir.

$ auxml backend \

  --infile <filename>
  --macros <filename>
  --build-type [web | android]
  --build-dir /path/to/build

'''



class CmdLine:
    already_initialized = False
    
    def __init__(self):
        if CmdLine.already_initialized:
            raise Exception("CmdLine object already initialized")
        self.args = {}
        self.parse_arguments()

    def check_to_help(self, args):
        for arg in args:
            if arg in ["-h", "--help", "help"]:
                self.help_message()
                sys.exit(0)
                
    def report_required(self, arg):
        self.err(f'  `{arg}` is a required argument')

    def store_option(self, args, option, argkey, msg):
        if option in args:
            idx = args.index(option)
            self.args[argkey] = self.get_value(args, option, msg)
            return True
        return False

    def get_value(self, args, option, msg):
        idx = args.index(option)
        if len(args) < idx+2:
            self.err(msg)
        return args[idx+1]
        
    
    def file_exists(self, key):
        fname = self.args[key]
        return (os.path.exists(fname), fname)
    
    def ensure_input_filename_option(self, args, option):
        op = f"-{option[2]}"
        if not (option in args or op in args):
            self.report_required(option)
        else:
            msg = f"filename after `{op}` is missing, you need to specify a filename"
            self.store_option(args, op, option[2:], msg)
            msg = f"filename after `{option}` is missing, you need to specify a filename"
            self.store_option(args, option, option[2:], msg)
            
            ok, name = self.file_exists(option[2:])
            if not ok:
                self.err(f"Could not find file: {name}")
            
    def ensure_output_path_option(self, args, option):
        if not (option in args):
            self.report_required(option)
        else:
            msg = f"path name after `{option}` is missing, you need to specify one"
            self.store_option(args, option, option[2:], msg)
        
    def store_buildtype(self, args):
        if not "--build-type" in args:            
            self.report_required("--build-type")
        else:
            msg = "build-type after `--build-type` is missing, options are [web | android]"
            self.store_option(args, "--build-type", "build-type", msg)            
            bt = self.args["build-type"]
            if bt not in ["web", "android"]:
                self.err(f"build-type needs to be `web` or `android`, got invalid: {bt}")
            
    def ensure_common_args(self, args):
        self.ensure_input_filename_option(args, "--infile")
        self.ensure_input_filename_option(args, "--macros")
                
    def do_backend(self, args):
        print(">> running backend")
        self.ensure_common_args(args)
        self.ensure_output_path_option(args, "--build-dir")
        self.store_buildtype(args)
        
    def do_singlefile(self, args):
        print(">>  running singlefile")
        self.ensure_common_args(args)
        self.ensure_output_path_option(args, "--outfile")

    def parse_arguments(self):
        args = sys.argv[1:]
        self.check_to_help(args)
        
        subcommand = args[0]
        if subcommand == "backend":
            self.do_backend(args)
        elif subcommand == "singlefile":
            self.do_singlefile(args)
        else:
            self.err("The first subcommand to auxml must be 'backend' or 'singlefile'")
        
        CmdLine.already_initialized = True

    def err(self,msg):
        print(msg)
        print()
        sys.exit(1)
        
    def help_message(self):
        print(HELPMSG)

    def setup_logging(self, loglevel):
        logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
        logging.basicConfig(level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

    def infile(self):
        return self.args["infile"]

    def macros(self):
        return self.args["macros"]
        
    def outfile(self):
        return self.args["outfile"]
    
    
cmdline = CmdLine()

