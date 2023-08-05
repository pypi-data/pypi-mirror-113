import sys
import os
import re
from pathlib import Path, PurePath
from json.decoder import JSONDecodeError

import obspy
from obspy.core.inventory import Inventory,  Station, Channel, Site
from obspy.core.inventory import Network as obspy_Network
from obspy.clients.nrl import NRL

from ..network import (Network)
from ..obsMetadata.obsmetadata import (ObsMetadata)
from ..misc.discoveryfiles import (Datapath)
import obsinfo 



# We'll first create all the various objects. These strongly follow the
# hierarchy of StationXML files.


def main():
    
    dp = Datapath()
    # create list of directories to search for files    
    verbose, print_output, test, validate, debug, input_filename, output_filename, schemapath = retrieve_arguments(dp)
        
    try:               
                         
        file = Path(input_filename).name    
       
        if validate:
            if verbose:
                print(f'Validating network file: {file}')
                
            ret = ObsMetadata().validate(schemapath,  str(input_filename), "yaml", 
                                         "network", verbose, "network", False)
                    
        info_dict = ObsMetadata.read_info_file(input_filename, dp)
        
        net_dict = info_dict.get('network',None)
        if not net_dict:
            return 
        
        if verbose:
            print(f'Processing network file: {file}')
        obj = Network(ObsMetadata(net_dict))
                  
        if verbose:
           print(f'Network file parsed successfully for: {file}')
           
        if print_output:
           print_network(obj, level)
        
        networks=[obj.obspy_network]
        if not isinstance(obj.obspy_network, obspy_Network):
            print("Not a network object")
    
        inv = Inventory(
                networks,
                # The source should be the id whoever create the file.
                source="ObsPy")
    
        if not test: # Generate Stationxml file
            stem_name = Path(file).stem      # remove .yaml
            stem_name = Path(stem_name).stem #Remove .network
            #stem_name = re.split("\\.", file)  #OJO Cambiar esto porque puede haber puntos antes
            output_filename = stem_name + ".station.xml"
            stationxml=inv.write(output_filename, format="stationxml", validate=False)
         
        if verbose:
           print(f'StationXML file created successfully: {output_filename}')        
               
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
    
  
def retrieve_arguments(datapath):
    
    options_dict = {
                       "output": "o",
                       "verbose" : "v",
                       "print_output" : "p",
                       "debug" : "d",
                       "test" : "t",
                       "validate" : "l",
                       "help" : "h",
                     }
    
    input_filename = output_filename = None
    verbose = print_output = test = False
    validate = debug = False
    skip_next_arg = False
    path_exists = False
            
    long_option = re.compile("^[\-][\-][a-zA-Z_]+$")
    short_option = re.compile("^[\-][a-zA-Z]$")
    possible_options = re.compile("^[vptldoh]+$")
    
    input_filename = ""
    
    option = None
    
    for arg in sys.argv[1:]:

        if skip_next_arg:
            skip_next_arg = False
            continue
        
        if re.match(long_option, arg):  
            option = options_dict.get(arg[2:])
        elif not arg[0] == "-":
                
                #parent = Path(arg).parent # If this is an absolute or relativa path
                #stem_file = Path(arg).name
               
                input_filename = str(datapath.build_datapath(arg))
                #sorted(parent.glob(stem_file))
                
                continue  
        else:
            option = arg[1:]
        
        if not re.match(possible_options, option):
            s = f'Unrecognized option in command line: -{option}\n'
            s += usage()
            raise ValueError(s)
        
        for opt in option:
    
            if opt == "o":
                if len(option) == 1:
                    output_filename = sys.argv[sys.argv.index("-o" if "-o" in sys.argv else "--output")+1]
                    skip_next_arg = True
                else:
                    warnings.warn('-o option should stand alone and be followed by a filename')
                    break
            elif opt == "v":
                verbose = True
            elif opt == "p":
                print_output = True
            elif opt == "d":
                debug = True  
            elif opt == "t":
                test = True
            elif opt == "l":
                validate = True
            elif opt == "h": 
                print(usage())
                sys.exit()
            
        skip_next_arg = False
    
    # schemas must always be installed under obsinfo/data/schemas   
    schemapath = Path(obsinfo.__file__).parent.joinpath('data', 'schemas')
    
    if not input_filename:
        print("No input filename specified")
        raise exit(1)
            
    return (verbose, print_output, test, validate, debug, input_filename, output_filename, schemapath)   

def usage():
    s = f'Usage: {sys.argv[0]} -vptldh  [-o <filename>] [-i] <filename>\n'
    s += f'Where:\n'
    s += f'      -v or --verbose: prints processing progression\n'
    s += f'      -p or --print_output: prints a human readable version of processed information file\n'
    s += f'      -t or --test: enters test mode, produces no output\n'
    s += f'      -l or --validate: validate the YAML or JSON format of the information file. Used when file syntax is trusted\n'
    s += f'      -h or --help: prints this message\n'
    s += f'      -o or --output: names the output file. Default is station.xml\n'
    s += f'      -i or --input: names the input file. The -i may be omitted and the argument will be understood as the input file name\n'
    
    
    return s
    
if __name__ == '__main__':
    main()