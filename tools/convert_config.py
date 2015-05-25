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
            
    
def convert_config(outFile, inFiles):
    
    inFileName = os.path.basename(inFiles[0])

    parameters = OrderedDict()  
    
    for inFile in reversed(inFiles):
        if os.path.exists(inFile):
            parameters.update(parse_config(inFile))


    write_config_header(outFile, inFileName.upper().replace('.','_'), parameters)
    




if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) >= 3:
        convert_config(sys.argv[1], sys.argv[2:])
    else:
        print('Invalid Number Of Arguments')