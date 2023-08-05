#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Functions to validate the lcheapo functions
There are two types of validating functionalities.
a) If the file name includes "test--attributes", ignore

b) If the file name is "normal", it will simply run through to make sure there are no errors  
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA @UnusedWildImport

import os
from pathlib import Path, PurePath
import glob
import inspect
import difflib
import re
import sys
from json.decoder import JSONDecodeError

from obspy.core.utcdatetime import UTCDateTime
# from pprint import pprint
# import xml.etree.ElementTree as ET
# from CompareXMLTree import XmlTree
from obsinfo.obsMetadata.obsmetadata import (ObsMetadata)
                                     #validate, _read_json_yaml,
                                     #ObsMetadata.read_json_yaml_ref, ObsMetadata.read_info_file)
# from obsinfo.info_dict import InfoDict
from obsinfo.instrumentation import (Instrumentation, InstrumentComponent,
                                     Datalogger, Preamplifier, Sensor,
                                     ResponseStages, Stage, Filter)
from obsinfo.instrumentation.instrumentation import (Location)
from obsinfo.network import (Station, Network)
from obsinfo.instrumentation.filter import (Filter, PolesZeros, FIR, Coefficients, ResponseList,
                     Analog, Digital, AD_Conversion)
from obsinfo.misc.printobs import  (PrintObs)
from obsinfo.misc.discoveryfiles import Datapath
import obsinfo 
from obsinfo.obsMetadata.obsmetadata import ObsMetadata
from obsinfo.misc.discoveryfiles import Datapath


class ValidateObsinfo():
    """
    Test suite for obsinfo operations.
    """
    def setUp(self, verbose=True, print_output=True, debug=False):
        
        dp = Datapath()
        self.datapath = dp
        self.datapath.infofiles_path = dp.datapath_list 
        self.datapath.validate_path = Path(obsinfo.__file__).parent.joinpath('data', 'schemas')
    
        self.verbose = verbose
        self.print_output = print_output
        self.debug = debug

    def assertTextFilesEqual(self, first, second, msg=None):
        with open(first) as f:
            str_a = f.read()
        with open(second) as f:
            str_b = f.read()

        if str_a != str_b:
            first_lines = str_a.splitlines(True)
            second_lines = str_b.splitlines(True)
            delta = difflib.unified_diff(
                first_lines, second_lines,
                fromfile=first, tofile=second)
            message = ''.join(delta)

            if msg:
                message += " : " + msg

            self.fail("Multi-line strings are unequal:\n" + message)

    def test_validate_json(self):
        """
        Test validation on a YAML file.

        The test file as an $ref to a file that doesn't exist, a field that
        is not specified in the the schema, and lacks a field required in
        the schema
        """
        test_file = PurePath(self.datapath.validate_path).joinpath( 'json_testschema.json')
        test_schema = PurePath(self.datapath.validate_path).joinpath(
                                   'json_testschema.schema.json')
        # self.assertFalse(validate(test_file, schema_file=test_schema,
        #                           quiet=True))

        # Run the code
        cmd = f'obsinfo-validate -s {test_schema} {test_file} > temp'
        os.system(cmd)

        # Compare text files
        self.assertTextFilesEqual(
            'temp',
            PurePath(self.datapath.validate_path).joinpath( 'json_testschema.out.txt')
            )
        os.remove('temp')
        
    def validate_all_filters(self):
        """
        Validate all information files in <component>/responses/_filters" subdirectory
        If you wish to test individual files, use test_filter(file) with file an absolute or 
        relative file name.
        """
        
        for dir in self.datapath.infofiles_path:
            files_in_validate_dir = Path(dir).joinpath(
                "*rs", # includes sensors, preamplifiers and dataloggers
                "responses",
                "filters/*.yaml")
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self.validate_filter(file)
        
    def validate_filters_in_directory(self, dir):
        """
        Validate all information files in filter directory.
        """
        if dir.is_dir():
            for file in dir.iterdir():
                self.validate_filter(file)     

    def validate_filter(self, info_file):
        """
        Validate a filter file. 
        """
        print(f'In validate all: {info_file}')      
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "filter", self.verbose, "filter", False)
            
        if ret and self.verbose:
           print(f'Filter test for: {info_file}: PASSED')
        
    def validate_all_stages(self):
        """
        Validate all information 
        files in each responses subdirectory.
        """
    
        for dir in self.datapath.infofiles_path:
            files_in_validate_dir = Path(dir).joinpath(
                "*rs", # includes sensors, preamplifiers and dataloggers
                "responses/*.yaml"
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self.validate_stage(file)
        
    def validate_stages_in_directory(self, dir):
        """
        Validate all information files in validate responses directory.
        """               
        datalogger_dir_re = re.compile(".*/dataloggers")
        sensor_dir_re = re.compile(".*/sensors")
        exception_re = re.compile(".*/test-with")
        
        if re.match(datalogger_dir_re, str(dir)) or re.match(sensor_dir_re, str(dir)):
            for file in (Path(dir).joinpath("responses")).iterdir():
                if not file.is_dir() and re.match(exception_re, str(file)) == None: 
                    self.validate_stage(file)        
        
    def validate_stage(self, info_file):
        """
        Test reading and converting to obspy a stage file with FIR filter.
        """
        
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "stage", self.verbose, "stage", False)
                
        if ret and self.verbose:
            print(f'Stage validate for: {info_file}: PASSED')
    
            
        
    def validate_all_components(self):
        """
        Test all information files in each responses subdirectory.
        """
        
        components_list = [
            "sensors",
            "preamplifiers",
            "dataloggers"
            ]
        
        for dir in self.datapath.infofiles_path:
            for comp in components_list:
                files_in_validate_dir = Path(dir).joinpath(
                    comp,
                    "*.yaml"  # includes sensors, preamplifiers and dataloggers
                    )
                
                filelist = glob.glob(str(files_in_validate_dir))
                
                for file in filelist:
                    ret = ObsMetadata().validate(self.datapath.validate_path, file, "yaml", comp, self.verbose, comp[:-1], False)
        
                    if ret and self.verbose:   
                        print(f'{file}: PASSED')
                    
        
    def validate_components_by_type(self, filelist):
        """
        Validate all information files in validate responses directory.
        """               
        datalogger_dir_re = re.compile("dataloggers")
        preamplifier_dir_re = re.compile("preamplifiers")
        sensor_dir_re = re.compile("sensors")

        for file in filelist:
            if re.match(datalogger_dir_re, str(filelist)):
                self.validate_datalogger(file)
                      
            elif re.match(preamplifier_dir_re, str(dir)):
                self.datapath.validate_preamplifier(file)
                      
            elif re.match(sensor_dir_re, str(dir)):
                self.validate_sensor(file)
                      
                
    def validate_datalogger(self, info_file):
        """
        Validate reading datalogger instrument_compoents.
        """
        
        #OJO: no configuraton passed from above. No delay_correction either.
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "datalogger", self.verbose, "datalogger", False)
        
        if ret and self.verbose:   
           print(f'{info_file}: PASSED')
           
           
    def validate_sensor(self, info_file):
        """
        Validate reading sensor instrument_compoents.
        """
        
        #OJO: no configuraton passed from above. No delay_correction either.
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "sensor", self.verbose, "sensor", False)
        
        if ret and self.verbose:   
           print(f'{info_file}: PASSED')
           
        
    def validate_preamplifier(self, info_file):
        """
        Validate reading sensor instrument_compoents.
        """
        
        #OJO: no configuraton passed from above. No delay_correction either.
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "preamplifier", self.verbose, "preamplifier", False)
        
        if ret and self.verbose:   
           print(f'{info_file}: PASSED')
           
           
    def validate_all_instrumentations(self, level="all"):
        """
        Validate all information files in each responses subdirectory.
        """
        
        for dir in self.datapath.infofiles_path:
            files_in_validate_dir = Path(dir).joinpath(
                "instrumentation/*.yaml" # includes sensors, preamplifiers and dataloggers
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self.validate_instrumentation(file)
                     
         
    def validate_instrumentation(self, info_file, level="all"):
        """
        Validate instrumentation.
        """
        
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "instrumentation", self.verbose, "instrumentation", False)
     
        if ret and self.verbose:   
           print(f'{info_file}: PASSED')
        
                     
    def validate_station(self, info_file='TEST.station.yaml', level="all"):
        """
        Validate a station.
        """
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "station", self.verbose, "station", False)
                
        if ret and self.verbose:
           print(f'Station validate for: {info_file}: PASSED')
           
           
    def validate_all_networks(self, level="all"):
        """
        Validate all information files in each responses subdirectory.
        """
        
        for dir in self.datapath.infofiles_path:
            files_in_validate_dir = Path(dir).joinpath(
                "network/*.yaml" # includes sensors, preamplifiers and dataloggers
                )
            
            filelist = glob.glob(str(files_in_validate_dir))
            
            for file in filelist:
                self.validate_network(file)
                     
             
    def validate_network(self, info_file='BBOBS.INSU-IPGP.network.yaml', level="all"):
        """
        Validate reading a network.
        """
        
        ret = ObsMetadata().validate(self.datapath.validate_path, info_file, "yaml", "network", self.verbose, "network", False)
        
        if ret and self.verbose:
           print(f'Network validate for: {info_file}: PASSED')
           
def main():

    verbose, print_output, debug, input_filename = retrieve_arguments()
    val = ValidateObsinfo()
    val.setUp(verbose, print_output) 
    dp = Datapath() 
        
    try:               
        
        type = ObsMetadata.get_information_file_type(input_filename)
         
        if verbose:
            print(f'Validating {type} file: {input_filename}')
            
        if type == "filter":
            val.validate_filter(val.datapath.build_datapath(input_filename))
        elif type == "stage":
            val.validate_stage(val.datapath.build_datapath(input_filename))
        elif type == "datalogger":
            val.validate_datalogger(val.datapath.build_datapath(input_filename))
        elif type == "preamplifier":
            val.validate_preamplifier(val.datapath.build_datapath(input_filename))
        elif type == "sensor":
            val.validate_sensor(val.datapath.build_datapath(input_filename))
        elif type == "instrumentation":
            val.validate_instrumentation(val.datapath.build_datapath(input_filename))
        elif type == "station":
            val.validate_station(val.datapath.build_datapath(input_filename))
        elif type == "network":
            val.validate_network(val.datapath.build_datapath(input_filename))
                       
    except TypeError:
        if debug:
            raise
        print("Illegal format: fields may be missing or with wrong format in input file.")
    except (KeyError, IndexError):
        if debug:
            raise
        print("Illegal value in dictionary key or list index")
    except ValueError:
        if debug:
            raise
        print("An illegal value was detected")
    except (IOError, OSError, LookupError):
        if debug:
            raise
        print("File could not be opened or read")
    except FileNotFoundError:
        if debug:
            raise
        print("File could not be found")
    except JSONDecodeError:
        if debug:
            raise
        print("File format is not recognized as either JSON or YAML. Check syntax.") 


def retrieve_arguments():
    
    options_dict = {
                       "quite" : "q",
                       "print_output" : "p",
                       "debug": "d",
                       "help" : "h",
                     }
    
    input_filename = output_filename = None
    verbose = True
    print_output = debug = False
    
    long_option = re.compile("^[\-][\-][a-zA-Z_]+$")
    short_option = re.compile("^[\-][a-zA-Z]$")
    possible_options = re.compile("^[qdph]+$")
    
    input_filename = ""
    
    option = None
    
    for arg in sys.argv[1:]:

        
        if re.match(long_option, arg):  
            option = options_dict.get(arg[2:])
        elif not arg[0] == "-":
            input_filename = arg
            continue  
        else:
            option = arg[1:]
        
        if not re.match(possible_options, option):
            s = f'Unrecognized option in command line: -{option}\n'
            s += usage()
            raise ValueError(s)
        
        for opt in option:
    
            if opt == "q":
                verbose = False
            elif opt == "p":
                print_output = True
            elif opt == "d":
                debug = True
            elif opt == "h": 
                print(usage())
                sys.exit()
             
    return (verbose, print_output, debug, input_filename)   

def usage():
    s = f'Usage: {sys.argv[0]} -vpdh <filename>\n'
    s += f'Where:\n'
    s += f'      -v or --verbose: prints test results\n'
    s += f'      -p or --print_output: prints a human readable version of processed information file\n'
    s += f'      -d or --debug: do not catch exceptions to show error trace.\n'
    s += f'      -h or --help: prints this message\n'
    
    return s
    
    
if __name__ == '__main__':
    main()