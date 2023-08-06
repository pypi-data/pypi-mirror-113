import os
import sys
import site
import platform
from pathlib import Path

def setup_obsinfo():
    
    version = platform.python_version()
         
    dest_dir = sys.argv[1] if len(sys.argv) > 1 else ""
    user_site = site.getusersitepackages() 
    path_to_package = Path(user_site).joinpath("obsinfo")
    setup_script = path_to_package.joinpath("bin", "setup-obsinfo")
    examples_dir = path_to_package.joinpath("_examples", "Information_Files")
    #Passes first argument as directory to move files to, from dir is 
    os.system("sh " +  str(setup_script) + " " + str(examples_dir) + " " + dest_dir)
    
    