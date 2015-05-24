# -*- coding: utf-8 -*-
"""
Created on Sun May 24 11:56:19 2015

@author: Collin Boots
"""
import sys
import os
import contextlib
from collections import OrderedDict


def parse_config(inFile):
    params = OrderedDict()
    with open(inFile, 'r') as f:
        for line in f:
            trimmed = line.strip()
            if trimmed.startswith('#'):
                continue
            if len(trimmed) == 0:
                continue
            
            splits = trimmed.split('=')
            key = splits[0].strip()
            value = ('='.join(splits[1:])).strip()

            params[key] = value
            
            
    return params


def write_macro(outFile, prefix, key, value):
    outFile.write('#define %s_%s %s\n'%(prefix,key,value))
    
    
@contextlib.contextmanager
def write_include_guard(outFile, guard_name):
    
    outFile.write('#ifndef %s\n' % guard_name)
    outFile.write('#define %s\n\n' % guard_name)
    yield
    outFile.write('\n#endif %s\n' % guard_name)
    

    
def write_config_header(outFile, config_prefix, parameters):
    outDir = os.path.dirname(outFile)
    
    if not os.path.exists(outDir):
        os.makedirs(outDir)
        
    with open(outFile, 'w') as f:
    
        with write_include_guard(f, config_prefix):
            for param in parameters:
                write_macro(f, config_prefix, param, parameters[param])
            
    
def convert_config(inFile, outFile, defaultDirs=None):
    
    inFileName = os.path.basename(inFile)

    parameters = OrderedDict()  
    
    if defaultDirs is not None:
        for directory in defaultDirs:
            defaultConfig = os.path.join(directory,inFileName)
            if os.path.exists(defaultConfig):
                parameters.update(parse_config(defaultConfig))
    
    parameters.update(parse_config(inFile))

    basename = os.path.basename(inFile)
    write_config_header(outFile, basename.upper().replace('.','_'), parameters)
    




if __name__ == '__main__':
    if len(sys.argv) == 3:
        convert_config(sys.argv[1], sys.argv[2])
    elif len(sys.argv) >= 4:
        convert_config(sys.argv[1], sys.argv[2], sys.argv[3:])
    else:
        print('Invalid Number Of Arguments')